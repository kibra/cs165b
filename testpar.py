from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets.classification import ClassificationDataSet, SequenceClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.connections import FullConnection
from pybrain.structure.modules import TanhLayer, LSTMLayer

# Load Dataset.
ds = ClassificationDataSet(2, class_labels=['zero', 'one'])
ds.appendLinked((0, 0), 0)
ds.appendLinked((0, 1), 0)
ds.appendLinked((1, 0), 1)
ds.appendLinked((1, 1), 0)

# Load Dataset.
sds = SequenceClassificationDataSet(1, 1)
sds.appendLinked(0, 0)
sds.appendLinked(0, 0)
sds.newSequence()
sds.appendLinked(0, 0)
sds.appendLinked(1, 0)
sds.newSequence()
sds.appendLinked(1, 0)
sds.appendLinked(0, 1)
sds.newSequence()
sds.appendLinked(1, 0)
sds.appendLinked(1, 0)
sds.newSequence()

print ds['input']
print ds['target']

print sds['input']
print sds['target']


# Build a recurrent Network.
net = buildNetwork(2, 3, 1)

rnet = buildNetwork(1, 3, 1, bias=True,
hiddenclass=LSTMLayer,
outclass=TanhLayer,
recurrent=True)

recCon = FullConnection(rnet['out'], rnet['hidden0'])
rnet.addRecurrentConnection(recCon)
rnet.sortModules()

print "------Before Training:"

print net.activate((0, 0))
print net.activate((0, 1))
print net.activate((1, 0))
print net.activate((1, 1))

print net['in']
print net['hidden0']
print net['out']

rnet.activate(0)
print rnet.activate(0)
rnet.reset()

rnet.activate(0)
print rnet.activate(1)
rnet.reset()

rnet.activate(1)
print rnet.activate(0)
rnet.reset()

rnet.activate(1)
print rnet.activate(1)
rnet.reset()

print rnet['in']
print rnet['hidden0']
print rnet['out']

print

#trainer = BackpropTrainer(net, ds, learningrate=0.05)
#trainer.trainEpochs(1000)

trainer = BackpropTrainer(rnet, sds, learningrate=0.01)
trainer.trainEpochs(5000)

print "------After Training:"

print net.activate((0, 0))
print net.activate((0, 1))
print net.activate((1, 0))
print net.activate((1, 1))
print net['in']
print net['hidden0']
print net['out']

rnet.activate(0)
print rnet.activate(0)
rnet.reset()

rnet.activate(0)
print rnet.activate(1)
rnet.reset()

rnet.activate(1)
print rnet.activate(0)
rnet.reset()

rnet.activate(1)
print rnet.activate(1)
rnet.reset()

print rnet['in']
print rnet['hidden0']
print rnet['out']

# Create a trainer for backprop and train the net.
