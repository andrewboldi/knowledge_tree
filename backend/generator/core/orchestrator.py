"""Knowledge generation orchestrator - alternating forward/backward passes."""

from .forward_pass import ForwardPass
from .backward_pass import BackwardPass


class Orchestrator:
    """Orchestrates alternating 10% forward/backward knowledge generation passes."""

    def __init__(self):
        self.forward_pass = ForwardPass()
        self.backward_pass = BackwardPass()

    def run(self, target_terms: int, domains: list[str]):
        """
        Run knowledge generation with strict alternating passes.

        Each pass processes 10% of target terms, alternating between
        forward (expand from axioms) and backward (trace prerequisites).
        """
        batch_size = int(target_terms * 0.10)
        current = 0
        pass_type = "forward"

        while current < target_terms:
            terms_this_batch = min(batch_size, target_terms - current)

            if pass_type == "forward":
                added = self.forward_pass.execute(domains, terms_this_batch)
                pass_type = "backward"
            else:
                added = self.backward_pass.execute(domains, terms_this_batch)
                pass_type = "forward"

            current += added
            print(f"Pass: {pass_type}, Added: {added}, Total: {current}/{target_terms}")
