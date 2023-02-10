class ReadRaDec(GenericPE):

    def __init__(self):
        GenericPE.__init__(self)
        self._add_output('output')
    def _process(self, inputs):
        file = inputs['input']
        print('Reading file %s' % file)
        with open(file) as f:
            count = 0
            for line in f:
                count+= 1
                ra, dec = line.strip().split(',')
                self.write('output', [count, ra, dec, 0.001])
