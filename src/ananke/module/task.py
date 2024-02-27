# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    task.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/02 12:26:26 by Winshare To       #+#    #+#              #
#    Updated: 2023/12/02 17:04:45 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ananke.module import Module, APIS, Template, TempStorage, DataFrameworkClient

# 1. LocalContentInteractionTask
class LocalContentInteractionTask(Module):
    """- 1. "LocalContentInteractionTask":
    Primarily responsible for interacting with information stored in temporary memory, including historical dialogues.
    Supports actions such as adding, deleting, searching, and changing.
    IntentObjectType: <context, document, multimodal-data>
    """

    def __init__(self):
        # Initialize any necessary local content state here
        super().__init__()


# 2. SystemCommandExecutionTask
class SystemCommandExecutionTask(Module):
    """- 2. "SystemCommandExecutionTask":
    Primarily responsible for executing specific commands, limited to the given system commands.
    Includes actions like deleting, publishing, sharing, scheduling, building, analyzing, and extending.
    IntentObjectType: <mission, document, multimodal-data>
    """

    def __init__(self):
        # Initialize any necessary system command state here
        super().__init__()


# 3. DataFrameworkIndexingTask
class DataFrameworkIndexingTask(Module):
    """- 3. "DataFrameworkIndexingTask":
    Primarily responsible for interacting with designated data frameworks, including querying, logical inference,
    math computing, and knowledge representation.
    IntentObjectType: <entity, logic_expression, math_expression, document, user_context, multimodal-data>
    """

    def __init__(self):
        # Initialize any necessary data framework state here
        super().__init__()


# 4. GenerationInteractionTask
class GenerationInteractionTask(Module):
    """- 4. "GenerationInteractionTask":
    Primarily responsible for generating tasks according to specific task templates.
    The template includes blog, presentation, paper, review, homework, book, document, code_generate, math_expression, logic_solver.
    IntentObjectType: <mission, entity, logic_expression, math_expression, document, user_context, multimodal-data>
    """

    def __init__(self):
        # Initialize any necessary generation task state here
        super().__init__()


TaskCollection = {
    "LocalContentInteractionTask": LocalContentInteractionTask,
    "DataFrameworkIndexingTask": DataFrameworkIndexingTask,
    "GenerationInteractionTask": GenerationInteractionTask,
    "SystemCommandExecutionTask": SystemCommandExecutionTask,
}


class ContentInteraction(LocalContentInteractionTask):
    """Utilizes fixed short-term storage for interaction, maintaining the full lifecycle of temporary content.
    Includes operations on temporary storage and automation of infinite-length temporary storage structures.
    """

    def __init__(self, core_object: TempStorage, **kwargs):
        super().__init__(**kwargs)


class FoundationAction(SystemCommandExecutionTask):
    """Initialized with a fixed library of APIs, then executes specific API calls based on the given intent.
    Differentiates between APIs within the system and operating system-level APIs, as well as third-party APIs for automated inclusion in the library.
    """

    def __init__(self, core_object: APIS, **kwargs):
        super().__init__(**kwargs)


class DataConference(DataFrameworkIndexingTask):
    """Initialized with a fixed data framework client, then performs operations on the data framework based on intent.
    Includes collaborative indexing of vectors, graphs, and relational data from the data framework.
    Also involves automated strategies for adding, deleting, searching, and changing.
    """

    def __init__(self, core_object: DataFrameworkClient, **kwargs):
        super().__init__(**kwargs)


class ModularizationGeneration(GenerationInteractionTask):
    """Generates content modularly based on templates.
    For example, for an article, each component requires collaboration with temporary storage or data framework data for modular generation.
    Both the structure and behavior of each part are controlled and defined by the template system.
    """

    def __init__(self, core_object: Template, **kwargs):
        super().__init__(**kwargs)

