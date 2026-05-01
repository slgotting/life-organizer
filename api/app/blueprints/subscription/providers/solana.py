
from app.blueprints.subscription.providers.provider import Provider

class Solana(Provider):

    def change_plan(self, plan):
        print(f'\nsubscribed to {plan}\n', flush=True) # print flush snippet