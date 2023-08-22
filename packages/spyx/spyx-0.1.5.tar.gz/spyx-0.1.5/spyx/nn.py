import jax
import jax.numpy as jnp
import haiku as hk
from .axn import Axon

# need to add shape checking/warning
def PopulationCode(num_classes):
    """
    Add population coding to the preceding neuron layer. Preceding layer's output shape must be a multiple of
    the number of classes. Use this for rate coded SNNs where the time steps are too few to get a good spike count.
    """
    def _pop_code(x):
        return jnp.sum(jnp.reshape(x, (-1,num_classes)), axis=-1)
    return jax.jit(_pop_code)

class ALIF(hk.RNNCore): 
    """
    Adaptive LIF Neuron based on the model used in LSNNs:

    Bellec, G., Salaj, D., Subramoney, A., Legenstein, R. & Maass, W. 
    Long short- term memory and learning-to-learn in networks of spiking neurons. 
    32nd Conference on Neural Information Processing Systems (2018).
    
    """


    def __init__(self, hidden_shape, beta=None, gamma=None, threshold=1,
                 activation = Axon(),
                 name="ALIF"):
        super().__init__(name=name)
        self.hidden_shape = hidden_shape
        self.beta = beta
        self.gamma = gamma
        self.init_threshold = threshold
        self.act = activation
    
    def __call__(self, x, VT):
        # this probably needs changed to be spltting an array
        V, T = jnp.split(VT, 2, -1)
        
        gamma = self.gamma
        beta = self.beta
        # threshold adaptation
        if not gamma:
            gamma = hk.get_parameter("gamma", self.hidden_shape, 
                                 init=hk.initializers.TruncatedNormal(0.25, 0.5))
            gamma = jax.nn.hard_sigmoid(gamma)
        if not beta:
            beta = hk.get_parameter("beta", self.hidden_shape, 
                                init=hk.initializers.TruncatedNormal(0.25, 0.5))
            beta = jax.nn.hard_sigmoid(beta)
        # calculate whether spike is generated, and update membrane potential
        thresh = self.init_threshold + T
        spikes = self.act(V - thresh)
        V = (beta*V + x - spikes*thresh).astype(jnp.float16)
        T = gamma*T + (1-gamma)*spikes
        
        VT = jnp.concatenate([V,T], axis=-1, dtype=jnp.float16)
        return spikes, VT
    
    # not sure if this is borked.
    def initial_state(self, batch_size):
        return jnp.zeros((batch_size,) + tuple(2*s for s in self.hidden_shape), dtype=jnp.float16)
         
class LI(hk.RNNCore):
    """
    Leaky-Integrate (Non-spiking) neuron model.

    Attributes:
        layer_size: Number of output neurons from the previous linear layer.

        beta: Decay rate on membrane potential (voltage). Set uniformly across the layer.
    """

    def __init__(self, layer_shape, beta=0.8, name="LI"):
        super().__init__(name=name)
        self.layer_shape = layer_shape
        self.beta = beta
    
    def __call__(self, x, Vin):
        # calculate whether spike is generated, and update membrane potential
        Vout = self.beta*Vin + x
        return Vout, Vout
    
    def initial_state(self, batch_size):
        return jnp.zeros((batch_size,) + self.layer_shape, dtype=jnp.float32)

class IF(hk.RNNCore): # bfloat16 covers a wide range of unused values...
    """
    Integrate and Fire neuron model 
    

    Attributes:
        hidden_size: Size of preceding layer's outputs
        threshold: threshold for reset. Defaults to 1.
        activation: spyx.activation function, default is Heaviside with Straight-Through-Estimation.
    """

    def __init__(self, hidden_shape, threshold=1, 
                 activation = Axon(),
                 name="LIF"):
        super().__init__(name=name)
        self.hidden_shape = hidden_shape
        self.threshold = threshold
        self.act = activation
    
    def __call__(self, x, V):
        # calculate whether spike is generated, and update membrane potential
        spikes = self.act(V - self.threshold)
        V = (V + x - spikes*self.threshold).astype(jnp.float16)
        
        return spikes, V

    def initial_state(self, batch_size): # figure out how to make dynamic...
        return jnp.zeros((batch_size,) + self.hidden_shape, dtype=jnp.float16)


class LIF(hk.RNNCore): # bfloat16 covers a wide range of unused values...
    """
    Leaky Integrate and Fire neuron model inspired by the implementation in
    snnTorch:

    https://snntorch.readthedocs.io/en/latest/snn.neurons_leaky.html
    

    Attributes:
        hidden_size: Size of preceding layer's outputs
        beta: decay rate. Set to float in range (0,1] for uniform decay across layer, otherwise it will be a normal
            distribution centered on 0.5 with stddev of 0.25
        threshold: threshold for reset. Defaults to 1.
        activation: spyx.activation function, default is Heaviside with Straight-Through-Estimation.
    """

    def __init__(self, hidden_shape: tuple, beta=None, threshold=1, 
                 activation = Axon(),
                 name="LIF"):
        super().__init__(name=name)
        self.hidden_shape = hidden_shape
        self.beta = beta
        self.threshold = threshold
        self.act = activation
    
    def __call__(self, x, V):
        
        # numerical stability gremlin...
        beta = self.beta
        if not beta:
            beta = hk.get_parameter("beta", self.hidden_shape, dtype=jnp.float16,
                                init=hk.initializers.TruncatedNormal(0.25, 0.5))
            beta = jax.nn.hard_sigmoid(beta)
            
        # calculate whether spike is generated, and update membrane potential
        spikes = self.act(V - self.threshold)
        V = (beta*V + x - spikes*self.threshold).astype(jnp.float16)
        
        return spikes, V

    def initial_state(self, batch_size): # figure out how to make dynamic...
        return jnp.zeros((batch_size,) + self.hidden_shape, dtype=jnp.float16)


class RLIF(hk.RNNCore): # bfloat16 covers a wide range of unused values...
    """
    Recurrent LIF Neuron adapted from snnTorch:

    https://snntorch.readthedocs.io/en/latest/snn.neurons_rleaky.html
    """

    def __init__(self, hidden_shape, beta=None, threshold=1,
                 activation = Axon(),
                 name="RLIF"):
        super().__init__(name=name)
        self.hidden_shape = hidden_shape
        self.beta = beta
        self.threshold = threshold
        self.act = activation
    
    def __call__(self, x, V):
        # calculate whether spike is generated, and update membrane potential
        recurrent = hk.get_parameter("w", self.hidden_shape, init=hk.initializers.TruncatedNormal())
        
        beta = self.beta
        if not beta:
            beta = hk.get_parameter("beta", self.hidden_shape, 
                                init=hk.initializers.TruncatedNormal(0.25, 0.5))
            beta = jax.nn.hard_sigmoid(beta)
        
        spikes = self.act(V - self.threshold)
        V = (beta*V + x + recurrent*spikes - spikes*self.threshold).astype(jnp.float16)
        
        return spikes, V

    def initial_state(self, batch_size):
        return jnp.zeros((batch_size,) + self.hidden_shape, dtype=jnp.float16)

# Current Based (CuBa)
class SC(hk.RNNCore): 
    """
    Conductance based neuron modeling synaptic conductance.

    Adapted from snnTorch:

    https://snntorch.readthedocs.io/en/latest/snn.neurons_synaptic.html
    """

    def __init__(self, hidden_shape, alpha=None, beta=None, threshold=1, 
                 activation = Axon(),
                 name="SC"):
        super().__init__(name=name)
        self.hidden_shape = hidden_shape
        self.alpha = alpha
        self.beta = beta
        self.threshold = threshold
        self.act = activation
    
    def __call__(self, x, VI):
        V, I = jnp.split(VI, 2, -1)
        
        alpha = self.alpha
        beta = self.beta
        # threshold adaptation
        if not alpha:
            alpha = hk.get_parameter("alpha", self.hidden_shape, 
                                 init=hk.initializers.TruncatedNormal(0.25, 0.5))
            alpha = jax.nn.hard_sigmoid(alpha)
        if not beta:
            beta = hk.get_parameter("beta", self.hidden_shape, 
                                init=hk.initializers.TruncatedNormal(0.25, 0.5))
            beta =jax.nn.hard_sigmoid(beta)
        # calculate whether spike is generated, and update membrane potential
        spikes = self.act(V - self.threshold)
        I = alpha*I + x
        V = (beta*V + I - spikes*self.threshold).astype(jnp.float16) # cast may not be needed?
        
        VI = jnp.concatenate([V,I], axis=-1, dtype=jnp.float16)
        return spikes, VI
    
    # this is probably borked with the shaping now.
    def initial_state(self, batch_size):
        return jnp.zeros((batch_size,) + tuple(2*s for s in self.hidden_shape), dtype=jnp.float16)
    
