import tensorflow as tf

class NeuralClassifier:
    def __init__(
        self,
        input_dim=2,
        num_hidden_units=4,
        hidden_layer_activation_function=tf.tanh,
        learning_rate=0.001,
        ):
        # Define network
        self.input_placeholder = tf.placeholder(
            dtype=tf.float32, shape=(None, input_dim))
        self.hidden_op = tf.layers.dense(
            inputs=self.input_placeholder,
            units=num_hidden_units,
            activation=hidden_layer_activation_function)
        self.logit_op = tf.layers.dense(inputs=self.hidden_op, units=1)
        self.predict_op = tf.sigmoid(self.logit_op)

        # Define loss and optimiser
        self.labels_placeholder = tf.placeholder(
            dtype=tf.float32, shape=(None, 1))
        self.loss_op = tf.losses.sigmoid_cross_entropy(
            self.labels_placeholder, self.logit_op)
        self.optimizer = tf.train.AdamOptimizer(learning_rate)
        self.train_op = self.optimizer.minimize(self.loss_op)
        # TODO: add accuracy op
        # accuracy = tf.reduce_mean(tf.cast(tf.equal(y, y_true), tf.float32)) # need y>.5

        # Create op for initialising variables
        self.init_op = tf.global_variables_initializer()

        # Create summaries, for visualising in Tensorboard
        # TODO: separate train and test loss
        tf.summary.scalar("Loss", self.loss_op)
        tf.summary.histogram("Hidden_layer_activations", self.hidden_op)
        tf.summary.histogram("Logits", self.logit_op)
        # tf.summary.scalar("Accuracy", accuracy)
        # tf.summary.histogram("Gradients", adam.compute_gradients(loss))
        self.merged_summary_op = tf.summary.merge_all()

    def initialize_variables(self, sess):
        sess.run(self.init_op)

    def predict(self, input_val):
        return self.predict_op.eval(
            feed_dict={self.input_placeholder: input_val})
    
    def training_step(self, sess, input_data, input_labels):
        train_loss_val, summary_val, _ = sess.run([
            self.loss_op,
            self.merged_summary_op,
            self.train_op],
            feed_dict={
                self.input_placeholder: input_data,
                self.labels_placeholder: input_labels})
        return train_loss_val, summary_val
        