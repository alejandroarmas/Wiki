---
layout: article
title: Markov Decision Processes
author:
  Alejandro Armas
tags:  Mathematics
aside:
    toc: true
---

First let's have a framework for what we would call randomness throughout time.

#### Stochastic Procesess 

A **Stochastic Process** is defined as a collection of [random variables](/2020/04/21/Distributions.html) $  \\{\\ X(t)\\}\_{t \in T}\ = \\{\\ x_1 , x_2 , \dots , x_T \\}\\ $ indexed by time (the subscript). When for all elements of this collection assume a value, we call each value in this trajectory a **state**. $ \textbf{S} = \\{\\ s_1 , s_2 , \dots , s_M \\}\\ $ There are **M** states in this collection, they are not always unique. From any timesteps $ x_{t} = w \to x_{t+1} = z$ we say the system made a transition from state $ w \to z$. Now if we were to compute the long term probability at time step $ n - 1$ we would need to compute $ P( x_{n+1} = i_{n + 1} \mid x_{n} = i_{n}, x_{n-1} = i_{n - 1}, \dots ,x_{0} = i_{0}) $

##### Markov Property

When we consider a Stochastic Process who's next state depends only on the current state (Markov Property) we say it is a Markov Process. In other words, the next state is conditionally independent of everything before the current state or said to be memoryless. Formally we write: 

$ P( x_{n+1} = i_{n + 1} \mid x_{n} = i_{n}) = P( x_{n+1} = i_{n + 1} \mid x_{n} = i_{n}, x_{n-1} = i_{n - 1}, \dots ,x_{0} = i_{0}) $

Furthermore, a **Markov Chain** is a Markov process limited to a discrete state space (There are a countable number of states) or a discrete indexing for each state in a trajectory. 

#### Quick Example 

Let us consider a naive model of a financial market who's quarterly (think every ~ 92 days) transitions are dictated by some probabilities we are assuming to be true. That is for every quarter that investors are bullish, we can say with 90% confidence the next quarter will be bullish. Think greedy for bullish and fear mongering for bear.  
<p>
    <img src="/assets/images/Markov/MarkovChain.png" alt="Markov Chain"/>
    <br>
    <em>Photo Courtesy of 
    <a href="https://towardsdatascience.com/introduction-to-markov-chains-50da3645a50d">[“Introduction to Markov Chains”]</a>
    </em>
</p>

It's a random process as far as we are concerned but it has the Markov Property so we can formulate a **one-state transition matrix**, where each row sums to one, to help us find useful things we may be interested in. 

Let:

$$
\boldsymbol{P} = 

\begin{pmatrix}
0.9 & 0.075 & 0.025\\
0.15 & 0.8 & 0.05 \\
0.25 & 0.25 & 0.5
\end{pmatrix}
$$

Remember the rows represent the current state you are in and the columns represent the state you are transitioning to. Let's say we are in the middle of a pandemic and the market reflects people's financial anxiety, then let's have our **initial state vector** be 

$$
\boldsymbol{s_0} = 

\begin{pmatrix}
0\\
1 \\
0 
\end{pmatrix}^T
$$

Which saids that there is a 100% probability we are in a bear market. If we wanted to know what the state of the economy was one quarter from now we perform [matrix multiplication](/2020/05/27/MatrixMultiplication.html):

$$
\boldsymbol{s_1} = 

\begin{pmatrix}
0\\
1 \\
0 
\end{pmatrix}^T

\begin{pmatrix}
0.9 & 0.075 & 0.025\\
0.15 & 0.8 & 0.05 \\
0.25 & 0.25 & 0.5
\end{pmatrix}

= 

\begin{pmatrix}
0.15\\
0.8 \\
0.05 
\end{pmatrix}^T
$$

#### Markov Reward Process

Say for example now, you are the manager of huge fund of money and had incentive to be in certain states of this financial market. There would be some positive reward for your porfolio (list of financial assets) if the state of the economy was a bull market and some negative reward if you were in a bear market. This problem could be formulated as a **Markov Reward Process**.

Let's denote a reward function $R(s)$ with values $R(\text{Bull}) = 4$, $R(\text{Bear}) = -2$, $R(\text{Stagnant}) = 0$ showing the monies (probabably in Millions) your hedgefund should be rewarded. Since states transition you into future states, we need some concept of potential future rewards we would recieve from a current state. Let's define a $ 0 \leq \gamma \leq 1$ term that discounts future rewards. 


Now we can define a Value Function for each state, $V(s) = R(s) + \gamma \sum_{s'} P(s' \mid s) V(s')$, which amounts to basically saying the value at the current state is the reward of the current state plus a discounted average value of the next state. This is because we do not want to be short sighted and consider only the immediate awards, while still maintaining some Furthermore if we choose $\gamma = 0.8$ we find that 

$$
\begin{align*}
V(\text{Bull}) &= 4 + 0.8 \big( 0.9 \times V(\text{Bull}) + 0.075 \times V(\text{Bear}) + 0.025 \times V(\text{Stagnant}) \big) \\

V(\text{Bear}) &= -2 + 0.8 \big( 0.15 \times V(\text{Bull}) + 0.8 \times V(\text{Bear}) + 0.05 \times V(\text{Stagnant}) \big) \\

V(\text{Stagnant}) &= 0 + 0.8 \big( 0.25 \times V(\text{Bull}) + 0.25 \times V(\text{Bear}) + 0.5 \times V(\text{Stagnant}) \big) \\


\end{align*}
$$

Solving this system of equations we arrive at the following computed Values: $V(\text{Bull}) = 15.4605$, $V(\text{Bear}) = 0.3289$, $V(\text{Stagnant}) = 6.5789$. 


#### Markov Decision Processes

A Markov Reward Process is a Markov Decision Process with a fixed policy $\pi(a \mid s)$. What this amounts to is that given a state $\pi$ tells you the probability we take an action given that state. In some cases, we have Markov Decision Processes without a policy and it is our task to find one. Some approaches include Policy iteration and Value iteration which rely on the Bellman Equations and discovering an optimal policy through dynamic programming or integer programming. 

### References

[1] [https://people.eecs.berkeley.edu/~pabbeel/cs287-fa12/slides/mdps-exact-methods.pdf](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa12/slides/mdps-exact-methods.pdf)

[2] [https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-825-techniques-in-artificial-intelligence-sma-5504-fall-2002/lecture-notes/Lecture20FinalPart1.pdf](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-825-techniques-in-artificial-intelligence-sma-5504-fall-2002/lecture-notes/Lecture20FinalPart1.pdf)

[3] [https://towardsdatascience.com/reinforcement-learning-demystified-markov-decision-processes-part-1-bf00dda41690](https://towardsdatascience.com/reinforcement-learning-demystified-markov-decision-processes-part-1-bf00dda41690)