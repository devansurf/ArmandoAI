import asyncio
import tensorflow as tf
import os
import numpy as np
from modules import utils as u

DIRECTORY = './history/{channel}.txt'

def loss(labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                batch_input_shape=[batch_size, None]),
        tf.keras.layers.LSTM(rnn_units,
                             return_sequences=True,
                             stateful=True,
                             recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size)
    ])
    return model
        
async def trainAI(ctx, epochSize):
    # Read, then decode for py2 compat.
 
    text = open(DIRECTORY.format(channel = ctx.guild.id), 'rb').read().decode(encoding='utf-8')
    vocab = sorted(set(text))
    # Creating a mapping from unique characters to indices
    char2idx = {u: i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)

    BATCH_SIZE = 64
    VOCAB_SIZE = len(vocab)  # vocab is number of unique characters
    EMBEDDING_DIM = 256
    RNN_UNITS = 1024

    # Buffer size to shuffle the dataset
    # (TF data is designed to work with possibly infinite sequences,
    # so it doesn't attempt to shuffle the entire sequence in memory. Instead,
    # it maintains a buffer in which it shuffles elements).
    BUFFER_SIZE = 10000

    checkpoint_dir = './checkpoints/{channel}'.format(channel = ctx.guild.id)

    epochSize = int(epochSize)
    def text_to_int(text):
        return np.array([char2idx[c] for c in text])

    text_as_int = text_to_int(text)

    def int_to_text(ints):
        try:
            ints = ints.numpy()
        except:
            pass
        return ''.join(idx2char[ints])

    print(int_to_text(text_as_int[:13]))

    seq_length = 100  # length of sequence for a training example
    # examples_per_epoch = len(text)//(seq_length+1)

    # Create training examples / targets
    char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

    sequences = char_dataset.batch(seq_length+1, drop_remainder=True)

    def split_input_target(chunk):  # for the example: hello
        input_text = chunk[:-1]  # hell
        target_text = chunk[1:]  # ello
        return input_text, target_text  # hell, ello

    # we use map to apply the above function to every entry
    dataset = sequences.map(split_input_target)
    data = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
    model = build_model(VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, BATCH_SIZE)
    # model.summary()

    # for input_example_batch, target_example_batch in data.take(1):
    #     # ask our model for a prediction on our first batch of training data (64 entries)
    #     example_batch_predictions = model(input_example_batch)
    #     # print out the output shape
    #     print(example_batch_predictions.shape,
    #         "# (batch_size, sequence_length, vocab_size)")

    

    model.compile(optimizer='adam', loss=loss)

    # Directory where the checkpoints will be saved
    
    # Name of the checkpoint files
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_prefix,
        save_weights_only=True)

    model.fit(data, epochs=epochSize, callbacks=[checkpoint_callback])

    # checkpoint_num = 10
    # model.load_weights(tf.train.load_checkpoint("./training_checkpoints/ckpt_" + str(checkpoint_num)))
    # model.build(tf.TensorShape([1, None]))



async def predict(ctx, inp):
    text = open(DIRECTORY.format(channel = ctx.guild.id), 'rb').read().decode(encoding='utf-8')
    vocab = sorted(set(text))
    # Creating a mapping from unique characters to indices
    char2idx = {u: i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)

    VOCAB_SIZE = len(vocab)  # vocab is number of unique characters
    EMBEDDING_DIM = 256
    RNN_UNITS = 1024
    checkpoint_dir = './checkpoints/{channel}'.format(channel = ctx.guild.id)


    def generate_text(model, start_string):
        # Evaluation step (generating text using the learned model)

        # Number of characters to generate
        num_generate = 800


        # Converting our start string to numbers (vectorizing)
        input_eval = [char2idx[s] for s in start_string]
        input_eval = tf.expand_dims(input_eval, 0)

        # Empty string to store our results
        text_generated = []

        # Low temperatures results in more predictable text.
        # Higher temperatures results in more surprising text.
        # Experiment to find the best setting.
        temperature = 0.9

        # Here batch size == 1
        model.reset_states()
        for i in range(num_generate):
            predictions = model(input_eval)
            # remove the batch dimension

            predictions = tf.squeeze(predictions, 0)

            # using a categorical distribution to predict the character returned by the model
            predictions = predictions / temperature
            predicted_id = tf.random.categorical(
                predictions, num_samples=1)[-1, 0].numpy()

            # We pass the predicted character as the next input to the model
            # along with the previous hidden state
            input_eval = tf.expand_dims([predicted_id], 0)

            text_generated.append(idx2char[predicted_id])

        return (start_string + ''.join(text_generated))

    channel = ctx.channel

    model = build_model(VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, batch_size=1)
    model.load_weights(tf.train.latest_checkpoint(checkpoint_dir)).expect_partial()
    model.build(tf.TensorShape([1, None]))

    
    #format the input to better suit discord chat
    formatted_inp = ctx.author.name + "\n" + inp
    print(formatted_inp)
    generated_text = await u.formatText(ctx, generate_text(model, formatted_inp))
    await channel.send("```" + ctx.author.name + "\n" + generated_text + "```")
    