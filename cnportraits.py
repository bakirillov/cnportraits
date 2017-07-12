"""
This is an implementation of an algorithm proposed in
"Portraits of complex networks" by Bagrow, Bollt, Scufca and ben-Abraham.
Arxiv link of their paper: https://arxiv.org/abs/cond-mat/0703470v2

Author of implementation:
Bogdan Kirillov (8k1r1ll0v@gmail.com, bakirillov@edu.hse.ru)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import argparse
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt
from os import walk, path, mkdir

GRAPH_EXTS = ["ncol", "graphml", "gml", "dot", "gv", "lgl", "net"]

class Portrait():

    def __init__(self, graph):
        self.g = graph

    @staticmethod
    def b2p(m):
        """Convert B-matrix to viewable picture"""
        y = m.shape[0]
        x = m.shape[1]
        lg = np.log(m+1)#+1 to get rid of infinities in log
        n = int(x/y)
        return(
            np.array([[lg[a,:]]*n for a in range(lg.shape[0])]).flatten().reshape((n*y, x))
        )

    def compute(self):
        """Compute portrait matrix (B)"""
        d = self.g.diameter()#Network diameter
        n = self.g.vcount()#Number of nodes
        self.B = np.zeros((d+1, n))
        maxPath = 1
        for s in range(n):
            nsPrev = 0
            maxPath = 1
            for l in range(d):
                ns = self.g.neighborhood_size(s, order=l)
                if l > 0:
                    #Since l-shell is a difference between
                    #the neighborhood of order at most l and
                    #of order at most l-1
                    ns -= nsPrev
                am = np.argmax(self.B[l,])
                #maximal path is l that is bigger than any other nonzero l
                maxPath = am if am > maxPath else maxPath
                nsPrev = ns
                self.B[l, ns] += 1
        self.B = self.B[:maxPath+1,:]#get the meaningful part of the matrix

    def draw(self):
        """Draw the portrait"""
        k = Portrait.b2p(self.B)
        self.I = plt.imshow(
            k, interpolation="nearest"
        )

    def saveMatrix(self, fn):
        """Save the matrix B as B.npy"""
        np.save(fn, self.B)

    def savePicture(self, fn):
        """Save the portrait as picture"""
        plt.savefig(fn)

def crop(ps):
    """Crops a list of portraits to (minY, minX) shape"""
    minyK = lambda x: x.B.shape[0]
    minxK = lambda x: x.B.shape[1]
    miny = min(ps, key=minyK).B.shape[0]
    minx = min(ps, key=minxK).B.shape[1]
    for a in ps:
        a.B = a.B[:miny,:minx]
    return(ps)
    

def startDrawing(args):
    """Portrait drawing routine"""
    P = Portrait(ig.load(args.graphF))
    P.compute()
    if args.modeV == "matrix":
        P.saveMatrix(args.outputF)
    elif args.modeV == "picture":
        P.draw()
        P.savePicture(args.outputF)

def startAnimating(args):
    """Animation routine. Currently outputs only jpeg frames instead of gif"""
    #global GRAPH_EXTS
    isgraph = lambda x: True if x.split(".")[-1] in GRAPH_EXTS else False
    files = list(
        map(
            lambda x: path.join(args.workingD, x),
            [a for a in walk(args.workingD)][0][2]
        )
    )
    portraits = [Portrait(ig.load(a)) for a in list(filter(isgraph, files))]
    pth = path.split(args.workingD)
    outDir = path.join(pth[0], pth[1]+"_animated")
    if not path.exists(outDir):
        mkdir(outDir)
    for i,a in enumerate(portraits):
        a.compute()
        a.draw()
        a.savePicture(path.join(outDir, str(i)+".png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help="Functions"
    )
    draw_parser = subparsers.add_parser(
        "draw", help="Draw a portrait for complex network"
    )
    draw_parser.add_argument(
        "graphF",
        metavar="Graph",
        action="store",
        help="Input file"
    )
    draw_parser.add_argument(
        "outputF",
        metavar="Portrait",
        action="store",
        help="Output picture or matrix"
    )
    draw_parser.add_argument(
        "modeV",
        metavar="Mode",
        action="store",
        help="Output mode",
        choices=["matrix", "picture"]
    )
    draw_parser.set_defaults(func=startDrawing)
    anim_parser = subparsers.add_parser(
        "animate", help="Compute an animation of a set of networks"
    )
    anim_parser.add_argument(
        "workingD",
        metavar="Directory",
        action="store",
        help="Input directory"
    )
    anim_parser.add_argument(
        "durationV",
        metavar="Duration",
        action="store",
        help="Duration of animation (Currently ignored)"
    )
    anim_parser.set_defaults(func=startAnimating)
    args = parser.parse_args()
    args.func(args)
