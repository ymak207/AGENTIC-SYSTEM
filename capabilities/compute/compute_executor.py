import re

from tools.calculator import calculate


class ComputeExecutor:

    def execute(
        self,
        step,
        state,
        user_goal
    ):

        state.add_trace(
            f"Compute capability started: {step['action']}"
        )

        expression = self._extract_expression(
            user_goal
        )

        result = calculate(
            expression
        )

        state.compute_results.append(
            {
                "expression": expression,
                "result": result
            }
        )

        state.add_trace(
            f"Computed {expression} = {result}"
        )

    # ---------------------------------------------

    def _extract_expression(
        self,
        text
    ):

        text = text.strip()

        #
        # Case 1
        # Pure expression
        #
        # 23*44
        # (18+5)/2
        #

        if re.fullmatch(
            r"[0-9\.\+\-\*\/\(\)\s]+",
            text
        ):
            return text

        #
        # Case 2
        #
        # calculate 23*44
        # what is 23*44
        # solve 55+12
        #

        matches = re.findall(

            r"[0-9\.\(\)\+\-\*\/ ]+[0-9\)]",

            text

        )

        if matches:

            return max(
                matches,
                key=len
            ).strip()

        raise Exception(
            "No mathematical expression found."
        )