from mlp import *
from morphs import *
from sql import *


#pos tags
#N(명사) V(용언) M(관형사,부사) J(조사) E(어미) X(접미사) S(부호)
tags = 'NVMJESX'


#data set
for i in range(1, 12):
    print(f'trying document_{i}')
    set_data(f'disk{i}.txt')
#x_train, x_test, y_train, y_test = prepare()

#train
#train(x_train, y_train, x_test, y_test)

#tensorboard
#use_tensorboard()
