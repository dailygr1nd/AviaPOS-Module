class MerchantHealthScore:

    def calculate(

        self,

        sales,

        debt,

        expenses

    ):

        score = 100

        if debt > sales:

            score -= 20

        if expenses > sales:

            score -= 20

        return max(

            score,

            0

        )