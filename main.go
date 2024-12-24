package main

import (
	"fmt"
	"log"

	"gobot.io/x/gobot/drivers/gpio"
	"gobot.io/x/gobot/platforms/raspi"
)

var (
	buttons = []string{"31", "33", "35", "37"}
	leds    = []string{"32", "36", "38", "40"}
)

type Batak struct {
	r       *raspi.Adaptor
	buttons []string
	leds    []*gpio.LedDriver
}

func NewBatak(buttons, leds []string) (batak *Batak, err error) {
	if len(buttons) != len(leds) {
		err = fmt.Errorf(
			"should have same numbers of buttons(%d) and leds(%d)",
			len(buttons), len(leds))
		return
	}
	batak = &Batak{
		r:       raspi.NewAdaptor(),
		buttons: make([]string, len(buttons)),
		leds:    make([]*gpio.LedDriver, len(leds)),
	}
	if err = batak.r.Connect(); err != nil {
		return
	}
	// Test buttons
	for i, button := range buttons {
		batak.buttons[i] = button
		if _, err = batak.r.DigitalRead(button); err != nil {
			err = fmt.Errorf("reading button %s:%s", button, err)
		}
	}
	// Start and Off leds
	for i, led := range leds {
		batak.leds[i] = gpio.NewLedDriver(batak.r, led)
		batak.leds[i].Start()
		batak.leds[i].Off()
	}
	return
}

func (b *Batak) Test() (err error) {
	var val int
	for {
		for i, button := range b.buttons {
			if val, err = b.r.DigitalRead(button); err != nil {
				err = fmt.Errorf("reading button %s(%d):%s", button, i, err)
				break
			}
			if val == 0 {
				b.leds[i].On()
			} else {
				b.leds[i].Off()
			}
		}
		if err != nil {
			break
		}
	}
	return
}

func main() {
	log.Println("Batak 4 started")
	batack, err := NewBatak(buttons, leds)
	if err != nil {
		log.Fatalf("Unable to start Batak:%s", err)
	}
	if err = batack.Test(); err != nil {
		log.Fatalf("Batak stopped on:%s", err)
	}
}
