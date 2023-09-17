#include <math.h>
#include "picosystem.hpp"
#include "hardware/structs/usb.h"

using namespace picosystem;

static bool use_usb_phy = false;
static bool use_usb_for_gpio = false;
static bool left = false, right = false;
static absolute_time_t start_time;

void init() {
  start_time = get_absolute_time();
}

void update(uint32_t tick) {
  if (!use_usb_phy &&
      absolute_time_diff_us(start_time, get_absolute_time()) > 50000 &&
      (usb_hw->sie_status & USB_SIE_STATUS_CONNECTED_BITS) == 0) {
    // Not connected to USB, engage phy override
    usb_hw->phy_direct_override = 0x11FC;
    use_usb_phy = true;
    start_time = get_absolute_time();
  }

  if (use_usb_phy && !use_usb_for_gpio && 
      ((usb_hw->phy_direct & 0x60000) == 0x60000)) {
    use_usb_for_gpio = true;
    hw_set_bits(&usb_hw->phy_direct, USB_USBPHY_DIRECT_TX_DP_OE_BITS | USB_USBPHY_DIRECT_TX_DM_OE_BITS);
  }

    left = button(LEFT);
    right = button(RIGHT);
  if (use_usb_for_gpio) {
    uint32_t val = (left ? 1 : 0) | (right ? 2 : 0);
    hw_write_masked(&usb_hw->phy_direct, val << USB_USBPHY_DIRECT_TX_DP_LSB, USB_USBPHY_DIRECT_TX_DP_BITS | USB_USBPHY_DIRECT_TX_DM_BITS);
  }
}

void draw(uint32_t tick) {
  pen(0, 0, 0);
  clear();

  if (use_usb_for_gpio) {
    pen(0, 200, 0);
  }
  else {
    pen(200, 0, 0);
  }
  if (left) {
    rect(0, 50, 20, 20);
  }
  if (right) {
    rect(100, 50, 20, 20);
  }
  
}