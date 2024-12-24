package main

import (
        "fmt"
        "log"
        "strings"
        "time"

        "gobot.io/x/gobot/drivers/gpio"
        "gobot.io/x/gobot/platforms/raspi"
)
var buttons = []string{
        "3", "5", "7", "8", "10", "24", "26", "29", "31",
}
func main() {
        r := raspi.NewAdaptor()
        r.Connect()
        for {
                var b strings.Builder
                for _, io := range buttons {
                        val, err := r.DigitalRead(io)
                        if err == nil {
                                fmt.Fprintf(&b, "%s %d ", io, val)
                        } else {
                                fmt.Fprintf(&b, "%s %d %s ", io, val, err.Error())
                        }
                }
                fmt.Println(b.String())
        }
        return
        led := gpio.NewLedDriver(r, "38")
        led.Start()
        led.Off()
        start := time.Now()
        count := 0
        for {
                if val, err := r.DigitalRead("37"); err == nil {
                        count++
                        if val == 1 {
                                led.Off()
                        } else {
                                led.On()
                        }
                        if time.Now().Sub(start).Seconds() > 1.0 {
                                log.Println(count, "read in 1s")
                                count = 0
                                start = time.Now()
                        }
                }
        }
        button := gpio.NewButtonDriver(r, "38", time.Millisecond)
        button.Start()

        buttonEvents := button.Subscribe()
        count = 0
        for {
                select {
                case event := <-buttonEvents:
                        count++
                        fmt.Println("Event:", count, event.Name, event.Data)
                        switch event.Name {
                        case gpio.ButtonPush:
                                led.Off()
                        case gpio.ButtonRelease:
                                led.On()
                        }
                }
        }
}