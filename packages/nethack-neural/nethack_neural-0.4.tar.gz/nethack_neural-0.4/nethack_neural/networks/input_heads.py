import torch
import torch.nn as nn

class GlyphHeadFlat(nn.Module):
    """A fully-connected model that takes a flattened glyph map as input.

    Attributes:
        device (str): The device to run the model on ('cpu' or 'cuda').
        hidden_size (int): The size of the hidden layers.
        fc1, fc2, fc3 (nn.Linear): The linear layers of the model.
    """
    def __init__(self, input_shape, output_shape, hidden_size=64, device='cpu'):
        super().__init__()
        input_shape = input_shape[0] * input_shape[1]
        self.device = device
        self.hidden_size = hidden_size
        self.fc1 = nn.Linear(input_shape, hidden_size, device=self.device)
        self.fc2 = nn.Linear(hidden_size, hidden_size, device=self.device)
        self.fc3 = nn.Linear(hidden_size, output_shape, device=self.device)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        value = self.fc3(x)
        return value

class BlstatsHead(nn.Module):
    """A fully-connected model that takes the 'blstats' (basic stats) as input.

    Attributes:
        input_shape (tuple): The shape of the input data.
        hidden_size (int): The size of the hidden layers.
        fc1, fc2, fc3 (nn.Linear): The linear layers of the model.
    """
    def __init__(self, input_shape, output_shape, hidden_size=64, device='cpu'):
        super().__init__()
        self.input_shape = input_shape[0]
        self.hidden_size = hidden_size
        self.fc1 = nn.Linear(self.input_shape, hidden_size, device=device)
        self.fc2 = nn.Linear(hidden_size, hidden_size, device=device)
        self.fc3 = nn.Linear(hidden_size, output_shape, device=device)

    def forward(self, x):
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        value = self.fc3(x)
        return value

class GlyphHeadConv(nn.Module):
    """A convolutional model that takes a glyph map as input.

    Attributes:
        device (str): The device to run the model on ('cpu' or 'cuda').
        input_shape (tuple): The shape of the input data.
        hidden_size (int): The size of the hidden layers.
        conv1, conv2 (nn.Conv2d): The convolutional layers of the model.
        fc1, fc2, fc3 (nn.Linear): The linear layers of the model.
    """
    def __init__(self, input_shape, output_shape, hidden_size=64, device='cpu'):
        super().__init__()
        self.device = device
        self.input_shape = input_shape
        self.hidden_size = hidden_size
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1, device=self.device)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1, device=self.device)
        self.fc1 = nn.Linear(32 * 21 * 79, hidden_size, device=self.device)
        self.fc2 = nn.Linear(hidden_size, hidden_size, device=self.device)
        self.fc3 = nn.Linear(hidden_size, output_shape, device=self.device)

    def forward(self, x):
        x = torch.tanh(self.conv1(x.unsqueeze(1)))
        x = torch.tanh(self.conv2(x))
        x = x.view(x.size(0), -1)
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        value = self.fc3(x)
        return value

class CartPoleHead(nn.Module):
    """A fully-connected model designed for the CartPole environment.

    Attributes:
        input_shape (tuple): The shape of the input data.
        hidden_size (int): The size of the hidden layers.
        fc1, fc2 (nn.Linear): The linear layers of the model.
    """
    def __init__(self, input_shape, output_shape, hidden_size=64, device='cpu'):
        super().__init__()
        self.input_shape = input_shape[0]
        self.hidden_size = hidden_size
        self.fc1 = nn.Linear(self.input_shape, hidden_size, device=device)
        self.fc2 = nn.Linear(hidden_size, output_shape, device=device)

    def forward(self, x):
        x = torch.tanh(self.fc1(x))
        x = self.fc2(x)
        return x

class ActivationWrapper(nn.Module):
    """A wrapper for adding an activation function to a model.

    Attributes:
        module (nn.Module): The module to apply the activation function to.
        activation (torch function): The activation function to apply.
    """
    def __init__(self, module, activation):
        super().__init__()
        self.module = module
        self.activation = activation

    def forward(self, x):
        x = self.module(x)
        x = self.activation(x)
        return x

class GlyphBlstatHead(nn.Module):
    """A model that takes both a glyph map and 'blstats' as input.

    Attributes:
        hidden_layer (int): The size of the hidden layer.
        device (str): The device to run the model on ('cpu' or 'cuda').
        glyph_head (GlyphHeadFlat or GlyphHeadConv): The model for processing the glyph map.
        blstats_head (BlstatsHead): The model for processing the 'blstats'.
        fc (nn.Linear): The final linear layer of the model.
        activation (torch function): The activation function of the model.
    """
    def __init__(self, glyph_shape, blstats_shape, output_shape, hidden_layer, actor=True, device='cpu') -> None:
        super().__init__()
        self.hidden_layer = hidden_layer
        self.device = device
        self.glyph_head = GlyphHeadFlat(glyph_shape, hidden_layer, hidden_size=hidden_layer, device=self.device)
        self.blstats_head = BlstatsHead(blstats_shape, hidden_layer, hidden_size=hidden_layer, device=self.device)
        self.fc = nn.Linear(2 * hidden_layer, output_shape, device=self.device)
        self.activation = nn.Softmax(dim=-1) if actor else nn.Identity()

    def forward(self, x):
        glyph = x['glyphs']
        blstats = x['blstats']
        glyph = self.glyph_head(glyph)
        blstats = self.blstats_head(blstats)
        x = torch.cat([glyph, blstats], dim=-1)
        x = self.fc(x)
        x = self.activation(x)
        return x