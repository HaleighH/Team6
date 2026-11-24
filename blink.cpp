#include <gpiod.hpp>
#include <iostream>
#include <chrono>
#include <thread>

constexpr int LED_PIN = 26; 

using namespace std;
using namespace gpiod;
using namespace std::chrono;
using namespace std::this_thread;

int main(int argc, char * argv[])
{
	// initialize gpiod
	chip chip("/dev/gpiochip0"); 
	auto request = chip.prepare_request() 
		.set_consumer("blink") 
		.add_line_settings(LED_PIN, line_settings().set_direction(line::direction::OUTPUT)) 
		.do_request();
	
	cout << "Blinking LED connected to GPIO pin " << LED_PIN << endl;
	
	while (true) // cntl c to end
	{
		request.set_value(LED_PIN, line::value::ACTIVE);
		sleep_for(milliseconds(500));
		
		request.set_value(LED_PIN, line::value::INACTIVE);
		sleep_for(milliseconds(500));
	}
	return 0;
}
