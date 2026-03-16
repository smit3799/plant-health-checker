import matplotlib.pyplot as plt
from CNN_model import *

# Plot accuracy
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.legend()
plt.show()

# Plot loss
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.legend()
plt.show()

# Notes:
# Looking for validation accuracy to keep going up.
# Would be overfitting if training accuracy goes up but validation accuracy goes down.
