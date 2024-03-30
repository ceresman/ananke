import json
import os
import time
import re
import warnings
from typing import List

import psutil
import subprocess
import logging
import threading

import lego_prover.utils as U
import pdb

class SubprocessMonitor:
    def __init__(
        self,
        commands: List[str],
        name: str,
        ready_match: str = r".*",
        log_path: str = "logs",
        callback_match: str = r"^(?!x)x$",  # regex that will never match
        callback: callable = None,
        finished_callback: callable = None,
        cwd: str = os.path.expanduser("~"),
        server_port: int = -1,
    ):
        self.commands = commands
        self.server_port = server_port
        start_time = time.strftime("%Y%m%d_%H%M%S")
        self.name = name
        if name == "isabelle_server":
            os.makedirs(f'logs/{name}/{start_time}_logs', exist_ok=True)
            self.logger = logging.getLogger(f'{name}-{server_port}')
            handler = logging.FileHandler(f"logs/{name}/{start_time}_logs/rank_{server_port}.log")
        else:
            self.logger = logging.getLogger(name)
            handler = logging.FileHandler(U.f_join(log_path, f"{start_time}.log"))
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.process = None
        self.ready_match = ready_match
        self.ready_event = None
        self.ready_line = None
        self.callback_match = callback_match
        self.callback = callback
        self.finished_callback = finished_callback
        self.thread = None
        self.cwd = cwd

    def _start(self):
        self.logger.info(f"Starting subprocess with commands: {self.commands}")
        print(self.commands, self.cwd)
        self.process = psutil.Popen(
            self.commands,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            universal_newlines=True,
            cwd=self.cwd
        )
        # pdb.set_trace()
        print(f"Subprocess {self.name} started with PID {self.process.pid}.")
        for line in iter(self.process.stdout.readline, ""):
            self.logger.info(line.strip())
            if re.search(self.ready_match, line):
                self.ready_line = line
                self.logger.info("Subprocess is ready.")
                print("Subprocess is ready.")
                self.ready_event.set()
                if "chroma" in self.name:
                    break
            if re.search(self.callback_match, line):
                self.callback()
        if not self.ready_event.is_set():
            self.ready_event.set()
            warnings.warn(f"Subprocess {self.name} failed to start.")
        if self.finished_callback:
            self.finished_callback()

    def run(self):
        self.ready_event = threading.Event()
        self.ready_line = None
        self.thread = threading.Thread(target=self._start)
        self.thread.start()
        self.ready_event.wait()

    def stop(self):
        self.logger.info("Stopping subprocess.")
        if self.process and self.process.is_running():
            self.process.terminate()
            self.process.wait()
    
    def terminate(self):
        parent = psutil.Process(self.process.pid)
        for child in parent.children(recursive=True):  # or parent.children() for recursive=False
            child.kill()
        parent.kill()

    def run_action(self, inputs):
        self.logger.info(f"Input: {inputs}")
        self.process.stdin.write(inputs + '\n')
        self.process.stdin.flush()

        for line in iter(self.process.stdout.readline, ""):
            self.logger.info(line)
            if line.startswith('{"error'):
                return json.loads(line)

    @property
    def is_running(self):
        if self.process is None:
            return False
        return self.process.is_running()

class Checker(object):
    """A modified version of the Draft, Sketch, Prove proof-checking client.
    (https://github.com/albertqjiang/draft_sketch_prove/blob/main/autoformalization/checker.py)

    This checker supports Isabelle2022 via the new version of PISA
    (https://albertqjiang.github.io/Portal-to-ISAbelle/).

    It supports checking a miniF2F-style proof via `check`.

    Finally, it replaces `sledgehammer` with a call to `normalhammer`.
    """

    def __init__(self, working_dir, isa_path, theory_file, port=9000):
        sys.path.append(os.environ["PISA_PATH"])
        try:
            from pisa_client import initialise_env

            self.initialise_env = initialise_env
            print(self.initialise_env)
        except:
            print("Set $PISA_PATH to /yourpath/to/Portal-to-ISAbelle/src/main/python")

        self.working_dir = working_dir
        self.isa_path = isa_path
        self.theory_file = theory_file
        self.port = port

    def _initialize(self):
        env = self.initialise_env(
            self.port,
            isa_path=self.isa_path,
            theory_file_path=self.theory_file,
            working_directory=self.working_dir,
        )
        return env

    def _exit(self, env):
        try:
            env.post("exit")
        except:
            print("env.post('exit') timed out")
            pass
        os.system(
            "ps aux | grep Isabelle | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1"
        )
        os.system(
            "ps aux | grep poly | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1"
        )

    def _parse_output(self, obs):
        """Parse the sledgehammer output, otherwise return an empty string"""
        if "<hammer>" in obs:
            output = obs.split("<hammer>")[0]
        else:
            output = ""
        return output

    def _run_step(self, step, i, tls_name, env):
        obs, reward, done, metadata = env.step_to_top_level_state(
            action=step, tls_name=tls_name, new_name="default_%d" % i
        )
        error = None
        if "error:" in obs or "Step error" in obs or "Unknown error" in obs:
            error = obs
        return obs, reward, done, metadata, error

    def _run_sledgehammer(self, step, i, tls_name, env):
        # First try heuristics
        for heuristic in [
            "by auto",
            "by simp",
            "by blast",
            "by fastforce",
            "by force",
            "by eval",
            "by presburger",
            "by sos",
            "by arith",
            "by linarith",
            "by (auto simp: field_simps)",
        ]:
            step_ = step.replace("normalhammer", heuristic)
            obs, reward, done, metadata, error = self._run_step(step_, i, tls_name, env)
            if error is None:
                obs = "%s <hammer> %s" % (heuristic, obs)
                return obs, reward, done, metadata, error
        # Try sledgehammer
        out = self._run_step(step, i, tls_name, env)
        return out

    def check(self, statement_and_proof):
        # Initialize environment
        env = self._initialize()
        env.initialise()

        # Wrap and parse theorem
        theory = Checker.wrap_theorem(statement_and_proof)
        steps = Checker.get_parsed(env, theory)

        result = self._check(env, steps)
        return result

    def _check(self, env, steps):
        done = False
        reason = ""
        success = False
        step_results = []
        tls_name = "default"
        for i, step in enumerate(steps):
            try:
                time0 = time.time()
                if "normalhammer" in step:
                    obs, reward, done, metadata, error = self._run_sledgehammer(
                        step, i, tls_name, env
                    )
                else:
                    obs, reward, done, metadata, error = self._run_step(
                        step, i, tls_name, env
                    )
                step_time = time.time() - time0
                step_results.append(
                    dict(
                        index=i,
                        step=step,
                        output=self._parse_output(obs),
                        step_time=step_time,
                    )
                )
                if error is not None:
                    reason = error
                    success = False
                    done = False
                    break
            except:
                # Timeout - end the proof attempt
                success = False
                done = False
                reason = "timeout (%d)" % len(step_results)
                step_results.append(dict(index=i, step=step, output=""))
                break

            # Change when successful
            tls_name = "default_%d" % i

        if done and reward == 1.0:
            success = True

        result = {
            "success": success,
            "reason": reason,
            "num_steps": len(steps),
            "last_step": len(step_results),
            "step_results": step_results,
            "theorem_and_proof": self.reconstruct(step_results) if success else "",
        }
        # Exit environment
        self._exit(env)
        return result

    @staticmethod
    def reconstruct(step_results):
        steps = []
        for step_result in step_results[1:]:
            if step_result["output"] != "":
                steps.append(step_result["output"].strip())
            else:
                steps.append(step_result["step"].strip())
        theorem_and_proof = "\n".join(steps)
        return theorem_and_proof

    @staticmethod
    def wrap_theorem(theorem):
        return (
            'theory Interactive imports HOL.HOL Complex_Main "HOL-Library.Code_Target_Numeral" "HOL-Library.Sum_of_Squares" "Symmetric_Polynomials.Vieta" "HOL-Computational_Algebra.Computational_Algebra" "HOL-Number_Theory.Number_Theory" \n begin\n%s'
            % theorem
        )

    @staticmethod
    def get_parsed(env, theory, tls_name="default"):
        # HACK: the parsing doesn't work well with `normalhammer`, so we replace
        # all hammer calls with sorry, then replace sorry to normalhammer after parsing.
        theory = theory.replace("sledgehammer", "sorry")
        theory = theory.replace("normalhammer", "sorry")

        steps = env.post(f"<parse text> ${theory}")
        steps = steps.split("<SEP>")
        steps = [s for s in steps if s.strip() != ""]
        # remove weird '$' step and whitespace steps
        steps = [s for s in steps if s != "$" and s.strip() != ""]
        steps = [s.replace("sorry", "normalhammer") for s in steps]
        return steps

import sys
import os
sys.path.append('../')
os.environ['PISA_PATH'] = '/root/Portal-to-ISAbelle/src/main/python'
from dsp_utils import Checker, LMFunctionAzure_Temp




class MathTheoremProvingService:
    def __init__(self, isa_path, theory_file, port=9000):
        self.isa_path = isa_path
        self.theory_file = theory_file
        self.port = port
        print(theory_file)

        # server_port = 8051
        self.isabelle_server = SubprocessMonitor(
                commands=[
                    "bash",
                    "run_server.sh",
                    str(port),
                ],
                name="isabelle_server",
                ready_match=r"Server is running. Press Ctrl-C to stop.",
                # log_path=U.f_join(self.log_path, "isabelle_server"),
                cwd=os.path.abspath("/root/Portal-to-ISAbelle"),
                server_port=port,
            )
        self.checker = Checker(
            working_dir=os.path.dirname(theory_file),
            isa_path=isa_path,
            theory_file=theory_file,
            port=port
        )


    # def isa_server():
        

    def generate_draft_sketch(self, informal_statement, formal_statement):
        '''
        step0 generate draft
        This function generates an *informal* proof $y_{I}\sim p(\cdot|x_I,P_{\text{draft}})$, called a *draft*.
        Here, $P_{\text{draft}}$ is a prompt containing examples of mapping the informal theorem statement $x_I$ to an informal proof $y_I$:
        
        step1 generate sketch:
        Generate a *formal sketch* $z_{F}\sim p(\cdot|y_{I}, x_I, x_F, P_{\text{sketch}})$
        Here, $P_{\text{sketch}}$ is a prompt containing the examples from the drafting step with an additional formal sketch.
        
        Parameters: 
        Informal_Statement: informal description for problem, like  'Show that if x is even, then x+5 is odd'
        Formal_Statement: formal description in term of Isabelle, like 
                            """theorem gcd_lcm:
                          assumes "gcd (n :: nat) 4 = 1" 
                              and "lcm (n :: nat) 4 = 28"
                          shows "n = 7"
                        proof -
                          have c1: "1*28 = n*4" using assms
                            sledgehammer
                          then have c2: "n = 1*28/4"
                            sledgehammer
                          then show ?thesis
                            sledgehammer
                        qed"""
        
        '''

        examples = [
    {"tag": "aimeI_2000_p7", "category": "algebra", "metadata": {}, "prompt": "Informal:\n(*### Problem\n\nSuppose that $x,$ $y,$ and $z$ are three positive numbers that satisfy the equations $xyz = 1,$ $x + \\frac {1}{z} = 5,$ and $y + \\frac {1}{x} = 29.$ Then $z + \\frac {1}{y} = \\frac {m}{n},$ where $m$ and $n$ are [[relatively prime]] positive integers. Find $m + n$. Show that it is 5.\n\n\nnote: this is the type of problem that makes you think symmetry, but actually can be solved easily with substitution, and other normal technniques\n\n### Solution\n\nWe can rewrite $xyz=1$ as $\\frac{1}{z}=xy$.\n\nSubstituting into one of the given equations, we have \n$x+xy=5$\n$x(1+y)=5$\n$\\frac{1}{x}=\\frac{1+y}{5}.$\n\nWe can substitute back into $y+\\frac{1}{x}=29$ to obtain\n$y+\\frac{1+y}{5}=29$\n$5y+1+y=145$\n$y=24.$\n\nWe can then substitute once again to get\n$x=\\frac15$\n$z=\\frac{5}{24}.$\nThus, $z+\\frac1y=\\frac{5}{24}+\\frac{1}{24}=\\frac{1}{4}$, so $m+n=005$.*)\n\nFormal:\ntheorem\n  fixes x y z :: real\n    and p :: rat\n  assumes \"0 < x \\<and> 0 < y \\<and> 0 < z\"\n    and \"x * y * z = 1\"\n    and \"x + 1 / z = 5\"\n    and \"y + 1 / x = 29\"\n    and \"z + 1 / y = p\"\n    and \"0 < p\" \n  shows \"let (m,n) = quotient_of p in m + n = 5\"\nproof -\n  (* We can rewrite $xyz=1$ as $\\frac{1}{z}=xy$. *)\n  have c0: \"z = 1 / (x*y)\"\n    sledgehammer\n  (* Substituting into one of the given equations, we have \n  $x+xy=5$\n  $x(1+y)=5$\n  $\\frac{1}{x}=\\frac{1+y}{5}.$ *)\n  have c1: \"1 / x = (1+y) / 5\" \n  proof -\n    have \"x + x * y = 5\" using assms(3) unfolding c0\n      sledgehammer\n    then have \"x * (1 + y) = 5\"\n      sledgehammer\n    then have t1: \"x = 5 / (1+y)\"\n      sledgehammer\n    then show ?thesis\n      sledgehammer\n  qed\n  (* We can substitute back into $y+\\frac{1}{x}=29$ to obtain\n  $y+\\frac{1+y}{5}=29$\n  $5y+1+y=145$\n  $y=24.$ *)\n  have \"y + (1+y)/5 = 29\" using assms(4) unfolding c1 sledgehammer\n  then have \"5* (y + (1+y)/5) = 5 * 29\" sledgehammer\n  also have \"... = 145\" sledgehammer\n  finally have c2_1: \"5* (y + (1+y)/5) = 145\" sledgehammer\n  have \"5* (y + (1+y)/5) = 5*y + (1+y)\" sledgehammer\n  also have \"... = 6*y + 1\" sledgehammer\n  finally have c2_2: \"5* (y + (1+y)/5) = 6*y + 1\" sledgehammer\n  have \"6*y + 1 = 145\" using c2_1 c2_2 sledgehammer\n  then have c2: \"y = 24\" sledgehammer\n  (* We can then substitute once again to get\n  $x=\\frac15$\n  $z=\\frac{5}{24}.$ *)\n  have \"1/x = 5\" using c1 unfolding c2 sledgehammer\n  then have c3: \"x = 1/5\"\n    sledgehammer\n  then have c4: \"z = 5/24\"\n    sledgehammer\n  (* Thus, $z+\\frac1y=\\frac{5}{24}+\\frac{1}{24}=\\frac{1}{4}$, so $m+n=005$. *)\n  have \"p = z + 1/y\" using assms(5) sledgehammer\n  also have \"... = 5/24 + 1/24\" unfolding c2 c4 sledgehammer\n  also have \"... = 1/4\" sledgehammer\n  finally have c5: \"p = 1/4\"\n    sledgehammer\n  have \"quotient_of p = (1, 4)\" unfolding c5 sledgehammer\n  then show ?thesis sledgehammer\nqed"},
    {"tag": "algebra_2rootsintpoly_am10tap11eqasqpam110", "category": "algebra", "metadata": {}, "prompt": "Informal:\n(*### Problem\n\nShow that for any complex number a, $(a-10)(a+11) = a^2 + a - 110$.\n\n### Solution\n\nWe first expand all terms of the left hand side to get $a^2 - 10a + 11a - 10*11$.\nThis equals $a^2 + a - 10*11 = a^2 + a - 110$.*)\n\nFormal:\ntheorem\n  fixes a :: complex\n  shows \"(a-10) * (a+11) = a^2 + a -110\"\nproof -\n  (* We first expand all terms of the left hand side to get $a^2 - 10a + 11a - 10*11$. *)\n  have \"(a-10) * (a+11) = a^2 - 10*a + 11*a - 10 *11\"\n    sledgehammer\n  (* This equals $a^2 + a - 10*11 = a^2 + a - 110$. *)\n  also have \"\\<dots> = a^2 + a - 10 * 11\"\n    sledgehammer\n  also have \"\\<dots> = a^2 + a - 110\"\n    sledgehammer\n  finally show ?thesis\n    sledgehammer\nqed"},
    {"tag": "mathd_numbertheory_335", "category": "number_theory", "metadata": {}, "prompt": "Informal:\n(*### Problem\n\nWhen Rachel divides her favorite number by 7, she gets a remainder of 5. What will the remainder be if she multiplies her favorite number by 5 and then divides by 7? Show that it is 4.\n\n### Solution\n\nLet $n$ be Rachel's favorite number. \nThen $n \\equiv 5 \\pmod{7}$, so $5n \\equiv 5 \\cdot 5 \\equiv 25 \\equiv 4 \\pmod{7}$.\n*)\n\nFormal:\ntheorem\n  fixes n :: nat\n  assumes h0 : \"n mod 7 = 5\"\n  shows \"(5 * n) mod 7 = 4\"\nproof -\n  (* Then $n \\equiv 5 \\pmod{7}$, so $5n \\equiv 5 \\cdot 5 \\equiv 25 \\equiv 4 \\pmod{7}$. *)\n  have c0:\"(5 * n) mod 7 = (5 * 5) mod 7\" using h0\n    sledgehammer\n  then have \"\\<dots> = 4\" sledgehammer\n  then have \"(5 * n) mod 7 = 4\" using c0 sledgehammer\n  then show ?thesis sledgehammer\nqed"}
]
        #Step 0: Generate a draft (informal proof)
        draft_prompt = """Draft an informal solution similar to below. 
        The informal solution will be used to sketch a formal Isabelle proof.
        Here are some examples:
        """
        for x in examples:
            draft_prompt += ("Example:\n" + x['prompt'][:x['prompt'].find('Formal:')] + "\n\n")
        draft_prompt += """Informal:
        (*### Problem
        
        """
        print("=================draft prompt==================")
        print(draft_prompt)
        print("=================draft prompt==================")
        
        api_key = "61bc1aab37364618ae0df70bf5f340dd"
        p_draft  = LMFunctionAzure_Temp(
            azure_endpoint="https://anankeus.openai.azure.com/",
            api_key=api_key,
            api_version="2024-02-15-preview"
        )
        draft_proof = p_draft.f(draft_prompt, informal_statement)
        print("=================informal statement==================")
        print(informal_statement)
        print("=================informal statement==================")
        print("=================draft proof==================")
        print(draft_proof)
        print("=================draft proof==================")


        #Step 1: Generate a formal sketch based on the draft
        # sketch prompt
        sketch_prompt = """Translate the informal solution into a sketch of the
        formal Isabelle proof. Add `sledgehammer` in the sketch whenever
        possible. `sledgehammer` will be used to call the automated Sledgehammer prover. 
        Here are some examples:
        """
        for x in examples:
            sketch_prompt += (x['prompt'] + "\n\n")
        sketch_prompt += """Informal:
        (*### Problem
        """
        print("=================sketch prompt==================")
        print(sketch_prompt)
        print("=================sketch prompt==================")

        # sketch llm
        p_sketch  = LMFunctionAzure_Temp(
            azure_endpoint="https://anankeus.openai.azure.com/",
            api_key=api_key,
            api_version="2024-02-15-preview"
        )

        # generate theorem with proof
        formal_statement = """theorem
        fixes x :: int
        assumes h0: "even x"
        shows "odd (x+5)" """
        print("=================formal statement==================")
        print(formal_statement)
        print("=================formal statement==================")
        
        text = p_sketch.f(sketch_prompt, 
                                        informal_statement + '\n\n' + 
                                        draft_proof + '\n\n' + 
                                        formal_statement ) #+ '\n\nFormal:\n\n'
        print("=================theorem with proof==================")
        print(text)
        print("=================theorem with proof==================")
        theorem_index = text.index('theorem')
        proof_index = text.index('proof -')
        qed_index = text.index('qed')
        theorem_with_proof = text[theorem_index:qed_index+3]
        
        # pattern = re.compile(r"(theorem .+?qed)", re.DOTALL)
        # match = pattern.search(theorem_with_proof)
        # theorem_with_proof = match.group(1)
        print("=================theorem with proof==================")
        print(theorem_with_proof)
        print("=================theorem with proof==================")

        
        return theorem_with_proof

    def check_conjectures(self, theorem_with_proof):
        '''
        Finally, we call [Sledgehammer](https://isabelle.in.tum.de/website-Isabelle2009-1/sledgehammer.html) to prove the remaining intermediate conjectures.
        You can see the completed proof printed in the output:

        theorem_with_proof combines theorem and proof together like 
            """theorem
            fixes x :: int
            assumes h0: "even x"
            shows "odd (x+5)"
            proof -
              (* If x is even, then it can be represented as 2n where n is some integer. *)
              obtain n where c1: "x = 2*n"
                using evenE assms
                sledgehammer
              (* So x + 5 equals 2n + 5. *)
              then have "x + 5 = 2*n + 5" 
                sledgehammer
              (* We can rewrite 2n + 5 as 2(n + 2) + 1, which is in the form of 2k + 1 where k is an integer (in this case, n + 2). Thus, x + 5 is odd. *)
              also have "\<dots> = 2*(n+2) + 1"
                sledgehammer
              then have exI: "\<exists>k. x + 5 = 2*k+1" 
                sledgehammer
              then have "odd (x+5)" 
                sledgehammer
              then show ?thesis 
                sledgehammer
            qed"""

        '''
        self.isabelle_server.run()

        print("====================================")
        print("====================================")
        print("====================================")
        print("====================================")
        print("====================================")
        print("====================================")
        print("====================================")
        print(theorem_with_proof)
        print("====================================")
        print("====================================")
        print("====================================")
        print("====================================")
        print("====================================")
        print("====================================")
        print("====================================")

        
        result = self.checker.check(theorem_with_proof)
        

        return result
        

# Example usage:
import sys
import os
sys.path.append('../')
os.environ['PISA_PATH'] = '/root/Portal-to-ISAbelle/src/main/python'
if __name__ == "__main__":
    isa_path='/root/Isabelle2022'
    theory_file='/root/Isabelle2022/src/HOL/Examples/Interactive.thy'
    port=8051
    service = MathTheoremProvingService(isa_path, theory_file, port)
    informal_statement = "Show that if x is even, then x+5 is odd"
    formal_statement = r"""theorem
    fixes x :: int
    assumes h0: "even x"
    shows "odd (x+5)"
    """
    theorem_with_proof = service.generate_draft_sketch(informal_statement, formal_statement)
    result = service.check_conjectures(theorem_with_proof)
    if result['success']:
            print("Proof successful:")
            print(result['theorem_and_proof'])
    else:
            print("Proof failed.")
    

#     # set server
# #     server_port = 8051
# #     isabelle_server = SubprocessMonitor(
# #             commands=[
# #                 "bash",
# #                 "run_server.sh",
# #                 str(server_port),
# #             ],
# #             name="isabelle_server",
# #             ready_match=r"Server is running. Press Ctrl-C to stop.",
# #             # log_path=U.f_join(self.log_path, "isabelle_server"),
# #             cwd=os.path.abspath("/root/Portal-to-ISAbelle"),
# #             server_port=server_port,
# #         )
# #     isabelle_server.run()

# #     checker = Checker(
# #     working_dir='/root/Isabelle2022/src/HOL/Examples',
# #     isa_path='/root/Isabelle2022',
# #     theory_file='/root/Isabelle2022/src/HOL/Examples/Interactive.thy',
# #     port=8051
# # )

#     theorem_and_sledgehammer_proof = """theorem gcd_lcm:
#       assumes "gcd (n :: nat) 4 = 1" 
#           and "lcm (n :: nat) 4 = 28"
#       shows "n = 7"
#     proof -
#       have c1: "1*28 = n*4" using assms
#         sledgehammer
#       then have c2: "n = 1*28/4"
#         sledgehammer
#       then show ?thesis
#         sledgehammer
#     qed"""
#     # result = checker.check(theorem_and_sledgehammer_proof)

#     # print("\n==== Success: %s" % result['success'])
#     # print("--- Complete proof:\n%s" % result['theorem_and_proof'])
   
#     isa_path='/root/Isabelle2022',
#     theory_file='/root/Isabelle2022/src/HOL/Examples/Interactive.thy'
#     port=8051
#     service = MathTheoremProvingService(isa_path, theory_file, port)
#     latex_statement = r"""theorem
#     fixes x :: int
#     assumes h0: "even x"
#     shows "odd (x+5)"
#     """
    
#     # Call the service to prove the theorem
#     # service.isa_prover()
#     zf = service.prove_theorem("Show that if x is even, then x+5 is odd", latex_statement)

    
#     result = checker.check(zf)
    

#     if result['success']:
#         print("Proof successful:")
#         print(result['theorem_and_proof'])
#     else:
#         print("Proof failed.")



