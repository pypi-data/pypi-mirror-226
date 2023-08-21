class Runner:
    def __init__(self, env, agent, loggers=[]):
        self.env = env
        self.agent = agent
        if loggers is None:
            loggers = []
        elif (isinstance(loggers, list) == False):
            loggers = [loggers]
        self.loggers = loggers
    
    def train(self, render=False):
        for episode in range(self.num_episodes):
            state = self.env.reset()
            done = False
            while not done:
                if render:
                    self.env.render()
                action = self.agent.act(state)
                next_state, reward, done, _ = self.env.step(action)
                self.agent.learning_step(state, action, reward, next_state, done)
                state = next_state
        self.agent.save('models/random_agent.pkl')

    def evaluate(self, render=False):
        self.agent.load('models/random_agent.pkl')
        total_reward = 0
        for episode in range(self.num_episodes):
            state = self.env.reset()
            done = False
            while not done:
                if render:
                    self.env.render()
                action = self.agent.act(state)
                next_state, reward, done, _ = self.env.step(action)
                total_reward += reward
                state = next_state
        self.log("Reward: {}".format(total_reward / self.num_episodes))

    def log(self, msg):
        for logger in self.loggers:
            logger.log(msg)

