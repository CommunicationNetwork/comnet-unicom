# Unicom
Unidirectional communication using an ESP8266 and RTOS SDK

Example transmitting:
```c
#include <unicom_transmitter.h>

void app_main() {
    uint8_t* buffer = init_transmitter("test-transmitter", 0x07, NULL);
    buffer[0] = 0xAA;
    buffer[1] = 0xBB;
    buffer[2] = 0xCC;
    
    esp_err_t code = transmit("test-receiver");
    if(code == ESP_OK) {
        ESP_LOGI("transmitter", "sent!");
    } else {
        ESP_LOGE("transmitter", "Error code: %x", code);
    }
}
```
