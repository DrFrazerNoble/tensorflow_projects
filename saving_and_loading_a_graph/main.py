'''graph_visualisation'''

# pylint: disable=E0401
# pylint: disable=C0103

# Import tensorflow to get access to tensorflow library
import os
import tensorflow as tf 

if not os.path.exists('./data/output'):
    os.makedirs('./data/output')

if not os.path.exists('./model'):
    os.makedirs('./model')

if not os.path.exists('./logs'):
    os.makedirs('./logs')
    
# Create placeholders as empty variables, which you send data to when evaluating the graph.
# The name_scope groups objects together. Here, the inputs A and B are in the 'input' name_scope.
with tf.name_scope('input'):
    A = tf.placeholder(tf.float32, shape=None, name='A')
    B = tf.placeholder(tf.float32, shape=None, name='B')

    # Here, we create scalar summaries, which record A's and B's values.
    tf.summary.scalar('A', A)
    tf.summary.scalar('B', B)

# Creates a simple graph, which adds two tensors.
# Here, the add operation and the output, C are in the 'output' name_scope.
with tf.name_scope('output'):

    C = tf.Variable(0, name='C')

    C = A + B

    #Here, we record C's value
    tf.summary.scalar('C', C)

# Create a session, which we use to evaluate the graph.
with tf.Session() as s:

    # Initialise global variables.
    s.run(tf.global_variables_initializer())

    # Create an object, which will record a summary.
    summary_writer = tf.summary.FileWriter('./logs', s.graph)

    # Merge all summaries together.
    merged = tf.summary.merge_all()

    # Evaluate the graph, providing A = 1.0 and B = 2.0.
    feed_dict = {A: 1.0, B: 2.0}
    summary, ans = s.run([merged, C], feed_dict)

    # Write summary to ./logs.
    summary_writer.add_summary(summary, 0)

    # Display answer on the console.
    print(ans)

    # To visualise output via TensorBoard, run: 'tensorboard --logdir=./logs'
    # and browse to, by default, 'localhost:6006'.

    # Save model to './model/'.
    saver = tf.train.Saver()
    saver.save(s, './model/main-0')
    saver.export_meta_graph('./model/main.meta')

with tf.Session() as l:

    # Here is a new session; which, is distinct from session s. So we don't have
    # access to the graph, as evaluated in s. The point is, the only way we have a graph
    # to evaluate is if we load it successfully from the meta file.

    # Load the model from './model'.
    loader = tf.train.import_meta_graph('./model/main.meta')
    loader.restore(l, './model/main-0')

    ans = l.run(C, {A: 2.0, B: 5.0})

    # Display answer on the console.
    print(ans)
