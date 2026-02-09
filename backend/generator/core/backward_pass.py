"""Backward pass - trace prerequisites from complex concepts."""


class BackwardPass:
    """Backward pass picks complex terms and traces their prerequisites."""

    def execute(self, domains: list[str], num_terms: int) -> int:
        """
        Execute backward pass: trace prerequisites of complex terms.

        Returns number of terms actually added.
        """
        raise NotImplementedError("Backward pass not yet implemented")
