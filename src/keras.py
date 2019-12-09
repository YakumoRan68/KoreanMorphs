from mlp import *
from morphs import *
from sql import *



def train_model():
    #load model
    x_train, x_test, y_train, y_test = prepare()

    #train
    train(x_train, y_train, x_test, y_test)

    #tensorboard
    use_tensorboard()


def classify(text, m):
    'classify text by m'
    #pos tags
    #N(명사) V(용언) M(관형사,부사) J(조사) E(어미) X(접미사) S(부호)
    tags = 'NVMJESX'
    morphs = Morphs()

    model = load_model(m)
    
    try:
        words = morphs.hannanum.morphs(text)
        result = []
        
        for word in words:
            w, y, left, right = get_data('dictionary', word)
            X=[[w, 0 if left=='' else int(left), 0 if right=='' else int(right)]]
            Y=[one_hot(y)]
            model.evaluate(X, Y)
            result.append((word, y))
        print(result)
    except Exception as e:
        print('dictionary에 매칭되지 않는 단어가 있어 종료합니다.', e)
        return


