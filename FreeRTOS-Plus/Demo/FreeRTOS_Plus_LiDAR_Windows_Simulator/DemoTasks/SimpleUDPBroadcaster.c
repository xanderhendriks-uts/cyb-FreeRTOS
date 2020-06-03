/*
 * FreeRTOS Kernel V10.3.0
 * Copyright (C) 2017 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * http://www.FreeRTOS.org
 * http://aws.amazon.com/freertos
 *
 * 1 tab == 4 spaces!
 */

/*
 * Creates two transmitting tasks and two receiving tasks.  The transmitting
 * tasks send values that are received by the receiving tasks.  One set of tasks
 * uses the standard API.  The other set of tasks uses the zero copy API.
 *
 * See the following web page for essential demo usage and configuration
 * details:
 * http://www.FreeRTOS.org/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.html
 */

/* Standard includes. */
#include <stdint.h>
#include <stdio.h>

/* FreeRTOS includes. */
#include "FreeRTOS.h"
#include "task.h"

/* FreeRTOS+TCP includes. */
#include "FreeRTOS_IP.h"
#include "FreeRTOS_Sockets.h"

#define simpTINY_DELAY	( ( TickType_t ) 2 )

/*
 * Uses a socket to send data without using the zero copy option.
 * prvSimpleServerTask() will receive the data.
 */
static void prvSimpleClientTask( void *pvParameters );

/*-----------------------------------------------------------*/

void vStartSimpleUDPBroadcasterTask( uint16_t usStackSize, uint32_t ulPort, UBaseType_t uxPriority )
{
	/* Create the client that broadcasts the pointcloud. */
	xTaskCreate( prvSimpleClientTask, "SimpCpyClnt", usStackSize, ( void * ) ulPort, uxPriority, NULL );
}
/*-----------------------------------------------------------*/

static void prvSimpleClientTask( void *pvParameters )
{
Socket_t xClientSocket;
struct freertos_sockaddr xDestinationAddress;
uint8_t cString[ 65 ];
BaseType_t lReturned;
uint32_t ulCount = 0UL, ulIPAddress;
const uint32_t ulLoopsPerSocket = 10UL;
const TickType_t x150ms = 150UL / portTICK_PERIOD_MS;

	/* Remove compiler warning about unused parameters. */
	( void ) pvParameters;

	/* This test sends to itself, so data sent from here is received by a server
	socket on the same IP address.  Setup the freertos_sockaddr structure with
	this nodes IP address, and the port number being sent to.  The strange
	casting is to try and remove compiler warnings on 32 bit machines. */
	xDestinationAddress.sin_addr = INADDR_BROADCAST;
	xDestinationAddress.sin_port = ( uint16_t ) ( ( uint32_t ) pvParameters ) & 0xffffUL;
	xDestinationAddress.sin_port = FreeRTOS_htons( xDestinationAddress.sin_port );

	for( ;; )
	{
		/* Create the socket. */
		xClientSocket = FreeRTOS_socket( FREERTOS_AF_INET, FREERTOS_SOCK_DGRAM, FREERTOS_IPPROTO_UDP );
		configASSERT( xClientSocket != FREERTOS_INVALID_SOCKET );

		/* The count is used to differentiate between different messages sent to
		the server, and to break out of the do while loop below. */
		ulCount = 0UL;

		do
		{
			/* Create the string that is sent to the server. */
			sprintf( ( char * ) cString, "Server received (not zero copy): Message number %lu\r\n", ulCount );

			/* Send the string to the socket.  ulFlags is set to 0, so the zero
			copy option is not selected.  That means the data from cString[] is
			copied into a network buffer inside FreeRTOS_sendto(), and cString[]
			can be reused as soon as FreeRTOS_sendto() has returned. */
			lReturned = FreeRTOS_sendto( xClientSocket, ( void * ) cString, strlen( ( const char * ) cString ), 0, &xDestinationAddress, sizeof( xDestinationAddress ) );

			ulCount++;

		} while( ( lReturned != FREERTOS_SOCKET_ERROR ) && ( ulCount < ulLoopsPerSocket ) );

		FreeRTOS_closesocket( xClientSocket );

		/* A short delay to prevent the messages printed by the server task
		scrolling off the screen too quickly, and to prevent reduce the network
		loading. */
		vTaskDelay( x150ms );
	}
}
/*-----------------------------------------------------------*/

