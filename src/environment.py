import numpy as np
from keras.layers import Input, Dense, Dropout, concatenate
from keras.models import Model, load_model
from keras.optimizers import Adam
from random import uniform, seed


def build_model(input_shapes, n_output):
    input_shape_time, input_shape_id = input_shapes

    x1 = Input(shape=input_shape_time)
    h1 = Dense(10, activation='relu', kernel_initializer='he_normal')(x1)
    # h1 = Dropout(0.5)(h1)

    x2 = Input(shape=input_shape_id)
    h2 = Dense(10)(x2)
    # h2 = Dropout(0.5)(h2)

    c = concatenate([h1, h2])
    h = Dense(6, activation='relu', kernel_initializer='he_normal')(c)
    # h = Dropout(0.5)(h)
    y = Dense(n_output, activation='linear', name='y')(h)

    return Model(
        inputs=[x1, x2],
        outputs=y,
        name='model')


def fit_transform(L, max_val, min_val):
    original = L.reshape(1, -1)[0]
    return (original - min_val) / (max_val - min_val)


class Env:
    def __init__(self, num_stations, num_devices_per_station):
        """model"""
        input_shape_time = (3, )
        input_shape_id = (1, )
        self.input_shapes = [input_shape_time, input_shape_id]
        self.output_shape = 1
        self.model = build_model(self.input_shapes, self.output_shape)
        self.model.compile(loss='mae', optimizer=Adam(), metrics=['mse', 'acc'])
        self.model = load_model('citibike_DNN_model.h5')

        """inference"""
        self.max_val, self.min_val = 3911, 72  # max: 3911 min: 72
        self.loss = 2

        """env"""
        self.num_stations, self.num_devices_per_station = num_stations, num_devices_per_station
        self.devices = [self.num_devices_per_station for _ in range(self.num_stations)]

    def reset(self):
        self.devices = [self.num_devices_per_station for _ in range(self.num_stations)]

    def incentive(self, time, stations, adj=True):  # time = [month, weekday, hour]
        times = np.array([time for _ in stations])
        ids = np.array([[e] for e in stations])
        refined_ids = fit_transform(ids.reshape(-1, 1), self.max_val, self.min_val)
        pred = self.model.predict([times, refined_ids])  # month, weekday, hour | id
        # print(pred)
        n_devices = [e[0] for e in pred.tolist()]

        if adj:
            # month, weekday, hour = time
            seed(time[0] * 1000 + time[1] * 100 + time[2])
            n_devices = [e + uniform(-self.loss, self.loss) for e in n_devices]  # Adjusting loss
        else:
            pass

        n_devices = [round(e) if e > 0 else round(e) - 1 for e in n_devices]  # Adjusting minus values
        # print(n_devices)

        return n_devices


if __name__ == "__main__":
    num_stations = 75
    num_devices_per_station = 10

    env = Env(num_stations, num_devices_per_station)
    print(env.incentive([12, 4, 6], [2800, 123, 458, 1311, 3000, 1]))
