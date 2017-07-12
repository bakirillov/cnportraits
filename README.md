# cnportraits - an implementation of Complex Network portraits algorithm    
      
Original algorithm was introduced by Bagrow, Bollt, Scufca and ben-Abraham in https://arxiv.org/abs/cond-mat/0703470v2   
Examples are given in the "Complex Network Portraits.ipynb" file.

Overall usage: cnportraits.py [-h] {draw,animate} ...   

positional arguments:   
*  {draw,animate}  Functions   
*    draw          Draw a portrait for complex network    
*    animate       Compute an animation of a set of networks    

optional arguments:    
*  -h, --help      show this help message and exit    

Drawing: cnportraits.py draw [-h] Graph Portrait Mode    

positional arguments:    
*  Graph       Input file    
*  Portrait    Output picture or matrix    
*  Mode        Output mode    

Animating: cnportraits.py animate [-h] Directory Duration     

positional arguments:   
*  Directory   Input directory    
*  Duration    Duration of animation (Currently ignored)    

## To do:
1. Distance computation as described in the paper;   
2. Animation of portrait changes given changes in the network structure;   
    * get the proper .gif generation working;  
