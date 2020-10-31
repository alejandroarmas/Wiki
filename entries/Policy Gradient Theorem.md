---
layout: article
title: Deriving Policy Gradient Theorem
author:
  Alejandro Armas
tags:  Mathematics Reinforcement-Learning Machine-Learning
aside:
    toc: true
---

Today we are going to derive an important result that provides a theoretical basis for a subset of the class of algorithms we call Reinforcement Learning (RL).

Particularly in RL, an agent, an entity which conducts actions in an environment, is incentivized to learn **quality sequential** decision making through exploration and exploitation. The way the agent learns from experience is by following a **policy** $\pi ( a \mid s )$, a principled guideline for which likely actions to take when faced with concrete situations. Situations could take many forms, right now you are probably sitting and reading this and that characterizes the state which you are in. Now continue reading or get up and do something, that is your decision and it will propel you into the next state. In the environment, the agent exhibits behaviors either using prior knowledge to exploit good decisions per the policy or exploration of the environment, gathering knowledge it uses to update it's policy. 

### Model Free
The challenge of RL sometimes is that the agent has no model (understanding) of the physical environment surrounding it. That is, it does not know how the environment will respond to the actions it engages in. A model predicts state transitions and rewards by some functions $P ( s_n \mid a_n , s_{n-1})$,  $P ( r_n \mid a_n , s_n)$ ). You know that if you see a lion and step close, it will likely eat you. Sometimes it's impossible for the agent to ever know this knowledge, therefore how could it learn good long term decisions (like never getting eaten lol) if it has no understanding of the physics that govern it's world?!?

## Derivation

Let $\tau = \\{ s_{1}, a_{1} , r_{1} , \dots \\}$ be the trajectory of some sequence of random variables denoting a specific order of states, actions and rewards.
Let $\pi \( \tau | \theta \)$ be the probability that a trajectory $\tau$ occurs under the policy of the agent described by the parametization $\theta$ and finally lets define the discounted reward function of the trajectory $R\(\tau) = \sum_{t = 1}^{T} \gamma^{t-1}r_{t}$ which gives us a metric of how well the trajectory $\tau$ is.


First consider the expectation of the return.

$$
\begin{align*}

E_{\tau \sim \pi_{\theta}}[R(\tau)] &= \int_{\tau} R(\tau) \pi ( \tau \mid \theta ) d\tau \\
\nabla_{\theta} E_{\tau \sim \pi_{\theta}}[R(\tau)] &= \nabla_{\theta} \int_{\tau} R(\tau) \pi ( \tau \mid \theta ) d\tau \\ 
&= \int_{\tau} R(\tau) \nabla_{\theta} \pi ( \tau \mid \theta ) d\tau \\


\end{align*}
$$

Also let us remember this rule from calculus.

$$
\begin{align*}
\frac{d}{dx}log\big(f(x)\big) &= \frac{f'(x)}{f(x)} \\
f(x)\frac{d}{dx}log\big(f(x)\big) &= f'(x) \\
\end{align*}
$$

Back to the Derivation...

$$
\begin{align*}

\nabla_{\theta} E_{\tau \sim \pi_{\theta}}[R(\tau)] &= \int_{\tau} R(\tau) \nabla_{\theta} \pi ( \tau | \theta ) d\tau \\
&= \int_{\tau} R(\tau) \pi ( \tau | \theta ) \nabla_{\theta}  log\big(\pi ( \tau | \theta )\big) d\tau \\
\nabla_{\theta} E_{\tau \sim \pi_{\theta}}[R(\tau)] &= E_{\tau \sim \pi_{\theta}}[R(\tau) \nabla_{\theta} log\big(\pi ( \tau | \theta )\big)]

\end{align*}
$$



Let us decompose $ \pi ( \tau \mid \theta ) $ into $n$ independent timesteps of temporally dependant probabilities. Basically every $ P(\\{ s_{1}, a_{1} , r_{1} \\}) $ depends on eachother, but are independent of the next subsequent timesteps.


$$
\begin{align*}

\pi ( \tau \mid \theta ) &= P(s_1) \pi ( a_1 \mid s_1 , \theta ) \underbrace{P ( r_1 \mid a_1 , s_1) P ( s_2 \mid a_1 , s_1)}_\text{Environment Stochasticity} \dots  P ( s_n \mid a_n , s_n) \pi ( a_{n} \mid s_{n} , \theta ) P ( r_n \mid a_n , s_n) \\
log[\pi ( \tau \mid \theta )]&= log[P(s_1) \pi ( a_1 \mid s_1 , \theta ) P ( r_1 \mid a_1 , s_1) P ( s_2 \mid a_1 , s_1) \dots  P ( s_n \mid a_n , s_{n-1}) \pi ( a_{n} \mid s_{n} , \theta ) P ( r_n \mid a_n , s_n)] \\ \\
\nabla_{\theta}log[\pi ( \tau \mid \theta )]&= \nabla_{\theta}log[P(s_1) \pi ( a_1 \mid s_1 , \theta ) P ( r_1 \mid a_1 , s_1) P ( s_2 \mid a_1 , s_1) \dots  P ( s_n \mid a_n , s_n) \pi ( a_{n} \mid s_{n} , \theta ) P ( r_n \mid a_n , s_n)] \\ \\
&= \nabla_{\theta}log[P(s_1)] +  \nabla_{\theta}log[\pi ( a_1 \mid s_1 , \theta )] +  \nabla_{\theta}log[P ( r_1 \mid a_1 , s_1)] + \nabla_{\theta}log[P ( s_2 \mid a_1 , s_1)] \dots\\ \\
&= \nabla_{\theta}log[\pi ( a_1 \mid s_1 , \theta )] + \nabla_{\theta}log[\pi ( a_2 \mid s_2 , \theta )]  + \dots + \nabla_{\theta}log[\pi ( a_n \mid s_n , \theta )]\\


\end{align*}
$$

Wow! Mathematically we have shown that if the agent wants to ascend the gradient to discover a "better" policy, then it does not need knowledge of the seemingly random world it lives in (i.e the state transition function $P ( s_n \mid a_n , s_{n-1})$ and state reward function $P ( r_n \mid a_n , s_n)$ ). Instead the agent only requires the rules which operate the agents decisions (i.e policy $\pi ( a \mid s )$ ). 


## References
Special thanks to Rylan Shaeffer for helping me so much to understand this topic, I wouldn't have been capable to have written this tutorial if it wasn't for him!

[https://lilianweng.github.io/lil-log/2018/02/19/a-long-peek-into-reinforcement-learning.html#policy-gradient](https://lilianweng.github.io/lil-log/2018/02/19/a-long-peek-into-reinforcement-learning.html#policy-gradient)

[https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html](https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html)

[https://rylanschaeffer.github.io/content/learning/reinforcement_learning.html](https://rylanschaeffer.github.io/content/learning/reinforcement_learning.html)