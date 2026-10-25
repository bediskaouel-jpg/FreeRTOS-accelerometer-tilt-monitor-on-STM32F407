/*
 * log.h
 */


#ifndef LOG_H_
#define LOG_H_
/*Include -----------------------------------------*/
#include "stdint.h"

#ifdef RELEASE
    #define DEBUG_LEVEL      ( 0U )
    #define DEBUG_RX         ( 0U )
    #define DEBUG_TX         ( 0U )

#else
    #define DEBUG_LEVEL      ( 0U )
    #define DEBUG_RX         ( 1U )
    #define DEBUG_TX         ( 1U )
    #define USE_TIMESTAMP    ( 1U )
#endif

/* DEBUG macros */

#define INTEGRATION_LOG( ... ) \
    do {                       \
        printf( __VA_ARGS__ ); \
    } while ( 0 )

#if ( DEBUG_LEVEL > 0U )
    #define  LOG( ... )        \
    do {                       \
        printf( __VA_ARGS__ ); \
        printf( "\n" );        \
    } while ( 0 )
#else
    #define LOG( ... )    do{} while( 0 )
#endif

#if ( DEBUG_LEVEL > 1U )

    #define  LOG_ERR( ... )    \
    do {                       \
        printf( "ERROR: " );   \
        printf( __VA_ARGS__ ); \
        printf( "\n" );        \
    } while ( 0 )
#else
    #define LOG_ERR( ... )    do{} while( 0 )
#endif

#if ( DEBUG_LEVEL > 2U )
    #define  LOG_DEBUG( ... )                            \
    do {                                                 \
        if( USE_TIMESTAMP == 1U ) {                      \
            int x = ( int ) HAL_GetTick();               \
            printf( "[%d.%03d]", x / 1000, x % 1000 ); } \
        printf( "DEBUG : " );                            \
        printf( __VA_ARGS__ );                           \
        printf( "\n" );                                  \
    } while ( 0 )
#else
    #define LOG_DEBUG( ... )    do{} while( 0 )
#endif /* if ( DEBUG_LEVEL > 2U ) */

#if ( DEBUG_TX > 0U )
    #define  LOG_TX( ... )        \
    do {                          \
        printf( "TX:====> ..." ); \
        printf( __VA_ARGS__ );    \
        printf( "\n" );           \
    } while ( 0 )
#else
    #define LOG_TX( ... )    do{} while( 0 )
#endif

#if ( DEBUG_RX > 0U )
    #define  LOG_RX( ... )        \
    do {                          \
        printf( "RX:<==== ..." ); \
        printf( __VA_ARGS__ );    \
        printf( "\n" );           \
    } while ( 0 )
#else
    #define LOG_RX( ... )    do{} while( 0 )
#endif

#ifdef DEBUG


/**
 * @brief Calculates the number of clock cycles spent executing a function.
 *
 * @note This function calculates the number of clock cycles spent executing a function since the specified start tick.
 *
 * @param tick_start The start tick value.
 *
 * @return The number of clock cycles spent executing the function.
 */
uint32_t debug_getFunction_executionClockCycle( uint32_t tick_start );

/**
 * @brief Gets the start time in clock cycles.
 *
 * This function retrieves the start time in clock cycles.
 *
 * @return The start time in clock cycles.
 */
uint32_t debug_getStartTime( void );


#endif /*DEBUG*/
/****************************************************************/

#endif /* UTILS_H_ */
