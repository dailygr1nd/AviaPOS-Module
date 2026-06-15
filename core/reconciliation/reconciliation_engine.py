class ReconciliationEngine:

    def reconcile(

        self,

        expected,

        actual

    ):

        matched = []

        missing = []

        for txn in expected:

            if txn in actual:

                matched.append(
                    txn
                )

            else:

                missing.append(
                    txn
                )

        return {

            "matched":
                matched,

            "missing":
                missing
        }