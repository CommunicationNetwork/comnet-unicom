# Unicom
Unidirectional communication using an ESP8266 and RTOS SDK.

This library can be used to transmit data between an ESP8266 and an OS supporting python scapy. 

## Transmitting
First, include the header file, which will include all the other header files needed.

`#include <unicom_transmitter.h>`

The function `init_transmitter` will initialize a buffer, set the channel and name. The function returns a pointer to the buffer.

`uint8_t* init_transmitter(char *id, uint8_t channel, freedom_outside_cb_t packet_sent_callback)`

After writing to the buffer it can be transmitted using the `transmit` function, which takes the name of the receiver and the size of the written data. This is needed so the library doesn't have to send the whole 2048 bytes but only the ones that were actually written. The receiver name will be used to generate a MAC, which is needed to filter out other packets by different transmitters during receiving.

`esp_err_t transmit(char* receiver, unsigned short size)`

Example transmitting:
```c
#include <unicom_transmitter.h>

void app_main() {
    uint8_t* buffer = init_transmitter("test-transmitter", 0x07, NULL);
    buffer[0] = 0xAA;
    buffer[1] = 0xBB;
    buffer[2] = 0xCC;
    
    esp_err_t code = transmit("test-receiver", 3);
    if(code == ESP_OK) {
        ESP_LOGI("transmitter", "sent!");
    } else {
        ESP_LOGE("transmitter", "Error code: %x", code);
    }
}
```

## Receiving
Receiving will be done using python and scapy.

First import the UnicomReceiver

`from unicom_receiver import UnicomReceiver`

To handle the received data, we have to create a receive callback. A simple one could look like this:
```
def recv(data):
    print(data)
```

The constructor of the UnicomReceiver looks like this:

`UnicomReceiver(interface, receiver_name, receivce_callback)`

To start the receiver, use `.start()`

Notice:
- The interface must be in monitor mode
- The received data starts with the length of the data (unsigned short, big endian)

Example receiving:
```python
from unicom_receiver import UnicomReceiver

def recv(data):
    print("Received packet!");
    print(data)

receiver = UnicomReceiver("interface", "test-receiver", recv)
receiver.start()
```
