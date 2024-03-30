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
        import pdb 
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
        self.checker = Checker(
            working_dir=os.path.dirname(theory_file),
            isa_path=isa_path,
            theory_file=theory_file,
            port=port
        )
    def isa_prover(self):
        theorem_and_sledgehammer_proof = """theorem gcd_lcm:
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
        result = self.checker.check(theorem_and_sledgehammer_proof)
        

        print("\n==== Success: %s" % result['success'])
        print("--- Complete proof:\n%s" % result['theorem_and_proof'])

    def prove_theorem(self, informal_statement, formal_statement):
        # Step 1: Generate a draft (informal proof)
        api_key = "61bc1aab37364618ae0df70bf5f340dd"
        p_draft  = LMFunctionAzure_Temp(
            azure_endpoint="https://anankeus.openai.azure.com/",
            api_key=api_key,
            api_version="2024-02-15-preview"
        )
        draft = p_draft.f("Draft an informal solution similar to below.", informal_statement)

        # Step 2: Generate a formal sketch based on the draft
        p_sketch  = LMFunctionAzure_Temp(
            azure_endpoint="https://anankeus.openai.azure.com/",
            api_key=api_key,
            api_version="2024-02-15-preview"
        )
        sketch_prompt = "Translate the informal solution into a sketch of the formal Isabelle proof."
        examples = [
            {"tag": "aimeI_2000_p7", "category": "algebra", "metadata": {}, "prompt": "Informal:\n(*### Problem\n\nSuppose that $x,$ $y,$ and $z$ are three positive numbers that satisfy the equations $xyz = 1,$ $x + \\frac {1}{z} = 5,$ and $y + \\frac {1}{x} = 29.$ Then $z + \\frac {1}{y} = \\frac {m}{n},$ where $m$ and $n$ are [[relatively prime]] positive integers. Find $m + n$. Show that it is 5.\n\n\nnote: this is the type of problem that makes you think symmetry, but actually can be solved easily with substitution, and other normal technniques\n\n### Solution\n\nWe can rewrite $xyz=1$ as $\\frac{1}{z}=xy$.\n\nSubstituting into one of the given equations, we have \n$x+xy=5$\n$x(1+y)=5$\n$\\frac{1}{x}=\\frac{1+y}{5}.$\n\nWe can substitute back into $y+\\frac{1}{x}=29$ to obtain\n$y+\\frac{1+y}{5}=29$\n$5y+1+y=145$\n$y=24.$\n\nWe can then substitute once again to get\n$x=\\frac15$\n$z=\\frac{5}{24}.$\nThus, $z+\\frac1y=\\frac{5}{24}+\\frac{1}{24}=\\frac{1}{4}$, so $m+n=005$.*)\n\nFormal:\ntheorem\n  fixes x y z :: real\n    and p :: rat\n  assumes \"0 < x \\<and> 0 < y \\<and> 0 < z\"\n    and \"x * y * z = 1\"\n    and \"x + 1 / z = 5\"\n    and \"y + 1 / x = 29\"\n    and \"z + 1 / y = p\"\n    and \"0 < p\" \n  shows \"let (m,n) = quotient_of p in m + n = 5\"\nproof -\n  (* We can rewrite $xyz=1$ as $\\frac{1}{z}=xy$. *)\n  have c0: \"z = 1 / (x*y)\"\n    sledgehammer\n  (* Substituting into one of the given equations, we have \n  $x+xy=5$\n  $x(1+y)=5$\n  $\\frac{1}{x}=\\frac{1+y}{5}.$ *)\n  have c1: \"1 / x = (1+y) / 5\" \n  proof -\n    have \"x + x * y = 5\" using assms(3) unfolding c0\n      sledgehammer\n    then have \"x * (1 + y) = 5\"\n      sledgehammer\n    then have t1: \"x = 5 / (1+y)\"\n      sledgehammer\n    then show ?thesis\n      sledgehammer\n  qed\n  (* We can substitute back into $y+\\frac{1}{x}=29$ to obtain\n  $y+\\frac{1+y}{5}=29$\n  $5y+1+y=145$\n  $y=24.$ *)\n  have \"y + (1+y)/5 = 29\" using assms(4) unfolding c1 sledgehammer\n  then have \"5* (y + (1+y)/5) = 5 * 29\" sledgehammer\n  also have \"... = 145\" sledgehammer\n  finally have c2_1: \"5* (y + (1+y)/5) = 145\" sledgehammer\n  have \"5* (y + (1+y)/5) = 5*y + (1+y)\" sledgehammer\n  also have \"... = 6*y + 1\" sledgehammer\n  finally have c2_2: \"5* (y + (1+y)/5) = 6*y + 1\" sledgehammer\n  have \"6*y + 1 = 145\" using c2_1 c2_2 sledgehammer\n  then have c2: \"y = 24\" sledgehammer\n  (* We can then substitute once again to get\n  $x=\\frac15$\n  $z=\\frac{5}{24}.$ *)\n  have \"1/x = 5\" using c1 unfolding c2 sledgehammer\n  then have c3: \"x = 1/5\"\n    sledgehammer\n  then have c4: \"z = 5/24\"\n    sledgehammer\n  (* Thus, $z+\\frac1y=\\frac{5}{24}+\\frac{1}{24}=\\frac{1}{4}$, so $m+n=005$. *)\n  have \"p = z + 1/y\" using assms(5) sledgehammer\n  also have \"... = 5/24 + 1/24\" unfolding c2 c4 sledgehammer\n  also have \"... = 1/4\" sledgehammer\n  finally have c5: \"p = 1/4\"\n    sledgehammer\n  have \"quotient_of p = (1, 4)\" unfolding c5 sledgehammer\n  then show ?thesis sledgehammer\nqed"},
            {"tag": "algebra_2rootsintpoly_am10tap11eqasqpam110", "category": "algebra", "metadata": {}, "prompt": "Informal:\n(*### Problem\n\nShow that for any complex number a, $(a-10)(a+11) = a^2 + a - 110$.\n\n### Solution\n\nWe first expand all terms of the left hand side to get $a^2 - 10a + 11a - 10*11$.\nThis equals $a^2 + a - 10*11 = a^2 + a - 110$.*)\n\nFormal:\ntheorem\n  fixes a :: complex\n  shows \"(a-10) * (a+11) = a^2 + a -110\"\nproof -\n  (* We first expand all terms of the left hand side to get $a^2 - 10a + 11a - 10*11$. *)\n  have \"(a-10) * (a+11) = a^2 - 10*a + 11*a - 10 *11\"\n    sledgehammer\n  (* This equals $a^2 + a - 10*11 = a^2 + a - 110$. *)\n  also have \"\\<dots> = a^2 + a - 10 * 11\"\n    sledgehammer\n  also have \"\\<dots> = a^2 + a - 110\"\n    sledgehammer\n  finally show ?thesis\n    sledgehammer\nqed"},
            {"tag": "mathd_numbertheory_335", "category": "number_theory", "metadata": {}, "prompt": "Informal:\n(*### Problem\n\nWhen Rachel divides her favorite number by 7, she gets a remainder of 5. What will the remainder be if she multiplies her favorite number by 5 and then divides by 7? Show that it is 4.\n\n### Solution\n\nLet $n$ be Rachel's favorite number. \nThen $n \\equiv 5 \\pmod{7}$, so $5n \\equiv 5 \\cdot 5 \\equiv 25 \\equiv 4 \\pmod{7}$.\n*)\n\nFormal:\ntheorem\n  fixes n :: nat\n  assumes h0 : \"n mod 7 = 5\"\n  shows \"(5 * n) mod 7 = 4\"\nproof -\n  (* Then $n \\equiv 5 \\pmod{7}$, so $5n \\equiv 5 \\cdot 5 \\equiv 25 \\equiv 4 \\pmod{7}$. *)\n  have c0:\"(5 * n) mod 7 = (5 * 5) mod 7\" using h0\n    sledgehammer\n  then have \"\\<dots> = 4\" sledgehammer\n  then have \"(5 * n) mod 7 = 4\" using c0 sledgehammer\n  then show ?thesis sledgehammer\nqed"}
        ]
        for example in examples:
            sketch_prompt += (example['prompt'] + "\n\n")
        sketch_prompt += "Informal:\n(*### Problem\n\n"
        sketch_prompt += draft + "\n\n"
        sketch_prompt += formal_statement + "\n*)"
        xi = 'Show that if x is even, then x+5 is odd'
        zf = p_sketch.f(sketch_prompt,xi)

        # Step 3: Use Sledgehammer to prove the remaining conjectures in the sketch
        result = self.checker.check(zf)

        # Return the result
        return result

# Example usage:
import sys
import os
sys.path.append('../')
os.environ['PISA_PATH'] = '/root/Portal-to-ISAbelle/src/main/python'
if __name__ == "__main__":
    # set server
    server_port = 8051
    isabelle_server = SubprocessMonitor(
            commands=[
                "bash",
                "run_server.sh",
                str(server_port),
            ],
            name="isabelle_server",
            ready_match=r"Server is running. Press Ctrl-C to stop.",
            # log_path=U.f_join(self.log_path, "isabelle_server"),
            cwd=os.path.abspath("/root/Portal-to-ISAbelle"),
            server_port=server_port,
        )
    isabelle_server.run()


    # checker = Checker(
        # working_dir='/root/Isabelle2022/src/HOL/Examples',
    isa_path='/root/Isabelle2022',
    theory_file='/root/Isabelle2022/src/HOL/Examples/Interactive.thy'
    # print(os.path.dirname(theory_file))
    port=8051
    # )

    # Initialize the service
    service = MathTheoremProvingService(isa_path, theory_file, port)

    # Example LaTeX input
    latex_statement = r"""theorem
    fixes x :: int
    assumes h0: "even x"
    shows "odd (x+5)"
    """
    
    # Call the service to prove the theorem
    service.isa_prover()
    # result = service.prove_theorem("Show that if x is even, then x+5 is odd", latex_statement)

    # Output the result
    if result['success']:
        print("Proof successful:")
        print(result['theorem_and_proof'])
    else:
        print("Proof failed.")