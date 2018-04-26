import tensorflow as tf
import tensorflow.contrib.eager as tfe
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def parse_csv(line):
    """parse the input csv file,
    1st feature is hashed name of the business, 2nd and 3nd are location,
    4th is number of reviews
    5th is the number of stars (label)
    """
    defaults = [[0.], [0.], [0.], [0.], [0]]  # sets field types
    parsed_line = tf.decode_csv(line, defaults)
    # First 4 fields are features, combine into single tensor
    features = tf.reshape(parsed_line[:-1], shape=(4,))
    # Last field is the label
    label = tf.reshape(parsed_line[-1], shape=())
    return features, label

def loss(model, x, y):
    """loss of the model"""
    y_ = model(x)
    return tf.losses.sparse_softmax_cross_entropy(labels=y, logits=y_)

def grad(model, inputs, targets):
    """calculate the gradient of the model"""
    with tfe.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
    return tape.gradient(loss_value, model.variables)

def pred(test_data):
    if type(test_data) is not list:
        return

    tf.enable_eager_execution()

    train_dataset_fp = os.path.join(APP_ROOT, 'csv_yelp.csv')

    train_dataset = tf.data.TextLineDataset(train_dataset_fp)
    train_dataset = train_dataset.skip(800)             # skip rows
    train_dataset = train_dataset.map(parse_csv)      # parse each row
    train_dataset = train_dataset.shuffle(buffer_size=1000)  # randomize
    train_dataset = train_dataset.batch(32)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation="relu", input_shape=(4,)),  # input shape required
        tf.keras.layers.Dense(10, activation="relu"),
        tf.keras.layers.Dense(6)
    ])

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)

    # keep results for debugging
    train_loss_results = []
    train_accuracy_results = []

    num_epochs = 201

    for epoch in range(num_epochs):
        epoch_loss_avg = tfe.metrics.Mean()
        epoch_accuracy = tfe.metrics.Accuracy()

      # Training loop - using batches of 32
        for x, y in tfe.Iterator(train_dataset):
        # Optimize the model
            grads = grad(model, x, y)
            optimizer.apply_gradients(zip(grads, model.variables),
                                      global_step=tf.train.get_or_create_global_step())

            # Track progress
            epoch_loss_avg(loss(model, x, y))  # add current batch loss
            # compare predicted label to actual label
            epoch_accuracy(tf.argmax(model(x), axis=1, output_type=tf.int32), y)

            # end epoch
            train_loss_results.append(epoch_loss_avg.result())
            train_accuracy_results.append(epoch_accuracy.result())

    # stars for prediction
    class_ids = ["0", "1", "2","3","4","5"]

    """predict the results with the current model"""
    predict_dataset = tf.convert_to_tensor([
        test_data
    ])

    predictions = model(predict_dataset)

    for i, logits in enumerate(predictions):
        class_idx = tf.argmax(logits).numpy()
        star = class_ids[class_idx]

    return star
