package main

import (
	"fmt"
	"log"
	"time"

	"github.com/reef-pi/rpi/i2c"
	rpio "github.com/stianeikeland/go-rpio/v4"
)

var (
	buttons = []int{26} // {"31", "33", "35", "37"}
	leds    = []int{21} // {"32", "36", "38", "40"}
)

type Batak struct {
	buttons []rpio.Pin
	leds    []rpio.Pin
}

func NewBatak(buttons, leds []int) (batak *Batak, err error) {
	if len(buttons) != len(leds) {
		err = fmt.Errorf(
			"should have same numbers of buttons(%d) and leds(%d)",
			len(buttons), len(leds))
		return
	}
	batak = &Batak{
		buttons: make([]rpio.Pin, len(buttons)),
		leds:    make([]rpio.Pin, len(leds)),
	}
	// Test buttons
	for i, button := range buttons {
		batak.buttons[i] = rpio.Pin(button)
		batak.buttons[i].Input()
	}
	// Start and Off leds
	for i, led := range leds {
		batak.leds[i] = rpio.Pin(led)
		batak.leds[i].Output()
		batak.leds[i].Low()
	}
	return
}

func (b *Batak) Test() (err error) {
	for {
		for i, button := range b.buttons {
			if button.Read() == rpio.Low {
				b.leds[i].High()
			} else {
				b.leds[i].Low()
			}
		}
		if err != nil {
			break
		}
		time.Sleep(time.Millisecond)
	}
	return
}

func main() {
	bus, err := i2c.New()
	if err != nil {
		log.Fatalln("new i2c", err)
	}
	h := NewHT16K33(bus, 0x71)
	if err := h.Setup(); err != nil {
		log.Fatalln("ht16k33 setup ", err)
	}
	if err := h.Display("    "); err != nil {
		log.Fatalln("display ", err)
	}
	return
	for b := 0; b <= 16*8; b++ {
		i:=b/8
		item := byte(1<<(b%8))
		for addr := 0; addr < len(h.buffer); addr++ {
			if addr == i {
				h.buffer[addr] = item
			} else {
				h.buffer[addr] = 0
			}
		}
		if err := h.bus.WriteToReg(h.addr, 0x00, h.buffer); err != nil {
			log.Fatal("display", err)
		}
		log.Println("byte", i, "bit", b)
		time.Sleep(time.Second)
	}
	return
	rpio.Open()
	defer rpio.Close()
	log.Println("Batak 4 started")
	batack, err := NewBatak(buttons, leds)
	if err != nil {
		log.Fatalf("Unable to start Batak:%s", err)
	}
	if err = batack.Test(); err != nil {
		log.Fatalf("Batak stopped on:%s", err)
	}
}
