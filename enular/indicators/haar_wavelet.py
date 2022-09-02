'''
Author: B. Bradford adapted from information provided by
        bearcave.com and Ian Kaplan.

MIT License

Copyright (c) B. Bradford

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


from backtrader.indicator import Indicator



# input lengths must be a power of two for haar with lifting:


class HaarLift(Indicator):

    lines = ('haarlift', )
    params = (('coefflev', None),
              ('coeffpick', None),
              ('blnincremental', False),
              ('threshlist', [1]))      #2**coefflev data points required or 2**coefflev

    plotinfo = dict(subplot=False)


    @staticmethod
    def next_power_of_2(x):
        return 1 if x == 0 else 2 ** (x.bit_length() -1)


    def once(self, start, end):
        self.blnforward = 1
        self.blninverse = 2

        #create dummy line to manipulate and desired 2** data length (max or selected)
        lstinputdata = self.data.array[:]                                   #make a copy of the list/array
                                                                            #max available data length
        if self.params.coefflev is None:                                    #input needs to be power of two data points
            pow2padding = self.next_power_of_2(len(lstinputdata))           #selected 2** from coefflev
       
        else:                                                               
            pow2padding = 2 ** self.params.coefflev
            
            if self.next_power_of_2(len(lstinputdata)) < pow2padding:
                raise ValueError("COEFF LEVEL %s GREATER THAN MAX DATA LENGTH %s AVAILABLE" % (
                                                        self.params.coefflev, self.next_power_of_2(len(lstinputdata))))

        if self.params.coefflev is None:
            self.params.coefflev = pow2padding.bit_length() - 1

        # If specific coeffpick selected set it to one, and others to zero:
        if self.params.coeffpick is not None:
            self.params.threshlist = [1] * self.params.coeffpick + [0] * (
            self.params.coefflev - self.params.coeffpick)

        dpcnt = len(lstinputdata) - pow2padding                             #only do loop once at end of array if blnincremental not true

        #Count backwards through line to leave most recent value in place if incremental:
        while dpcnt > 0:
            dpcnt -= 1                                                      #decrement immediately as list slicing is zero-based
            inlist = self.data.array[dpcnt:dpcnt + pow2padding]

            ftresult = HaarLift.forwardtrans(self, vec=inlist)            #forward transform

            threshedresult = HaarLift.wvltthreshold(coeffary=ftresult, threshlist=self.params.threshlist)

            itresult = HaarLift.inversetrans(self, vec=threshedresult)    #inverse transform

            dummyaryout = lstinputdata[:dpcnt] + itresult + lstinputdata[dpcnt + pow2padding:]
            lstinputdata = dummyaryout                                      # self.lines[0].array[pow2padding:] + itresult

            #Only run once if not doing incremental:
            if not self.params.blnincremental: break

        self.lines[0].array = lstinputdata


    def wvltthreshold(coeffary, threshlist):
        print ("waveletlifting:  len(coeffary).bit_length()", len(coeffary).bit_length())

        if len(coeffary).bit_length() < len(threshlist):
            raise ValueError('WARNING: THRESHOLD LIST LENGTH IS SMALLER THAN NUMBER OF COEFF LEVELS.')

        threshedresult = coeffary[:]

        for i in range(1, len(threshlist)):
            for x in range(2**i, 2**(i+1)):
                print ("waveletlifting:  i, x, len(threshlist)  ", i, x, len(threshlist))
                threshedresult[x] = coeffary[x] * threshlist[i]
        return threshedresult


    def split(vec, N):
        start = 1
        end = N - 1

        while (start < end):
            #Could do this with list comprehension, but want to stick to the original java structure:
            for i in range(start, end, 2):
                tmp = vec[i]
                vec[i] = vec [i + 1]
                vec[i+1] = tmp
            start += 1
            end -= 1
        return vec


    def merge(self, vec, N):
        half = N >> 1
        start = half-1
        end = half

        while (start > 0):
            for i in range(start, end, 2):
                tmp = vec[i]
                vec[i] = vec[i+1]
                vec[i+1] = tmp
            start -= 1
            end += 1


    def forwardtrans(self, vec):
        '''
        The result of forwardTrans is a set of wavelet coefficients
        ordered by increasing frequency and an approximate average
        of the input data set in vec[0].  The coefficient bands
        follow this element in powers of two (e.g., 1, 2, 4, 8...).
        '''

        N = len(vec)
        print ("forwardtrans N: ", N)
        #set for counter:
        n = N
        print ("forwardtrans  n:  ", n)

        while n > 1:
            print ("forwardtrans split...")
            vec = HaarLift.split(vec, n)
            print("forwardtrans predict...")
            vec = HaarLift.predict (self, vec, n, self.blnforward)
            print("update split...")
            vec = HaarLift.update (self, vec, n, self.blnforward)
            n = n >> 1
        return vec


    def inversetrans(self, vec):
        N = len(vec)
        n = 2

        while n <= N:
            HaarLift.update(self, vec, n, self.blninverse)
            HaarLift.predict (self, vec, n, self.blninverse)
            HaarLift.merge(self, vec, n)
            n = n << 1
        return vec


    def predict(self, vec, N, direction):
        half = N >> 1
        cnt = 0

        for i in range (0, half, 1):
            predictval = float(vec[i])
            j = int(i+half)

            if (direction == self.blnforward):
                vec[j] = vec[j] - predictval

            elif (direction == self.blninverse):
                vec[j] = vec[j] + predictval

            else:
                print("haar: predict: bad direction value")

        return vec


    def update(self, vec, N, direction):
        half = N >> 1

        for i in range (0, half, 1):
            j = int(i + half)
            updateVal = float(vec[j] / 2.0)

            if (direction == self.blnforward):
                vec[i] = vec[i] + updateVal

            elif (direction == self.blninverse):
                vec[i] = vec[i] - updateVal
                
            else:
                print("haar update: bad direction value")

        return vec