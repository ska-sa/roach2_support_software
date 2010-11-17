/*filename: cpld_decode.c revision 0
written by: vaughan moss and david george, 25/06/2010

this script opens a csv file (txt or csv) with values "sample, tms, tdi, tdo"
and stores the values into a struct (record).

file headers are then printed to both screen and a different ouput file, script then flows
through a jtag state(switch) machine which is fed the array value of tms, it appends the
current state of the state machine and the future state which it will go to.

The contents of the array are then printed to screen and the output file line by line
The output file is in csv format with columns, sample, tms, tdi, tdo, current state, future state
*/

#include <stdio.h>

//jtag state machine definitions
#define ST_TEST_LOGIC_RESET 0
#define ST_RUN_TEST_IDLE    1
#define ST_SELECT_DR_SCAN   2
#define ST_CAPTURE_DR       3
#define ST_SHIFT_DR         4
#define ST_EXIT1_DR         5
#define ST_PAUSE_DR         6
#define ST_EXIT2_DR         7
#define ST_UPDATE_DR        8
#define ST_SELECT_IR_SCAN   9
#define ST_CAPTURE_IR       10
#define ST_SHIFT_IR         11
#define ST_EXIT1_IR         12
#define ST_PAUSE_IR         13
#define ST_EXIT2_IR         14
#define ST_UPDATE_IR        15

const char *state_name_arr[] = { //array to convert to strings when writing states to file
  "TEST_LOGIC_RESET",
  "RUN_TEST_IDLE",
  "SELECT_DR_SCAN",
  "CAPTURE_DR",
  "SHIFT_DR",
  "EXIT1_DR",
  "PAUSE_DR",
  "EXIT2_DR",
  "UPDATE_DR",
  "SELECT_IR_SCAN",
  "CAPTURE_IR",
  "SHIFT_IR",
  "EXIT1_IR",
  "PAUSE_IR",
  "EXIT2_IR",
  "UPDATE_IR",
  NULL
};

struct record //structure for all data
{
  int spl, tms, tdi, tdo, current_state, future_state; 
};

int jtag_state = ST_TEST_LOGIC_RESET; //switch variable defaulted to reset state

int main(void)
{
  const char filename[] = "msr.txt"; //name of input file
  const char writefile[] = "msrstate.txt"; //name of output file

  FILE *file = fopen(filename, "r"); //open said file
  if ( file != NULL ) //open if file open successful
  {
    char line[80]; //think this is max length of line in file??
    struct record record[750]; //create record struct of 750, will need to change for big files!!
    size_t count, i = 0;
    while (i < sizeof record/sizeof *record)
    {
      if (fgets(line, sizeof line, file) == NULL)
      {
        break;
      }
      if (sscanf(line, "%d,%d,%d,%d", &record[i].spl, &record[i].tms,
        &record[i].tdi, &record[i].tdo) == 4) //reading in 4 variables here, seperated by commas
      {
        i++;
      }
    }
    fclose(file);
    printf("Sample,TMS,TDI,TDO,Current_State,Future_State\n"); //print headers to screen
    
//write headers to file
    FILE *output_file;
    output_file = fopen(writefile, "a+");
    fprintf(output_file, "Sample,TMS,TDI,TDO,Current_State,Future_State\n");
    //file is left open here and closed at the end of the for loop

    for (count = i, i = 0; i < count; ++i) //main for loop to run through rows in array
    {

//case structure
      switch (jtag_state) {

        case ST_TEST_LOGIC_RESET:
          record[i].current_state = jtag_state;
          if (!record[i].tms) {
            jtag_state = ST_RUN_TEST_IDLE;
            record[i].future_state = jtag_state;
          } else {
            record[i].future_state = jtag_state;
          }
          break;

        case ST_RUN_TEST_IDLE:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_SELECT_DR_SCAN;
            record[i].future_state = jtag_state;
          } else {
            record[i].future_state = jtag_state;
          }
          break;

        case ST_SELECT_DR_SCAN:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_SELECT_IR_SCAN;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_CAPTURE_DR;
            record[i].future_state = jtag_state;
          }
          break;

        case ST_CAPTURE_DR:
          record[i].current_state = jtag_state;
          if (!record[i].tms){
            jtag_state = ST_SHIFT_DR;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_EXIT1_DR;
            record[i].future_state = jtag_state;
          }
          break;

        case ST_SHIFT_DR:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_EXIT1_DR;
            record[i].future_state = jtag_state;
          } else {
            record[i].future_state = jtag_state;
          }
          break;

        case ST_EXIT1_DR:
          record[i].current_state = jtag_state;
          if (!record[i].tms){
            jtag_state = ST_PAUSE_DR;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_UPDATE_DR;
            record[i].future_state = jtag_state;
          }
          break;

        case ST_PAUSE_DR:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_EXIT2_DR;
            record[i].future_state = jtag_state;
          } else {
            record[i].future_state = jtag_state;
          }
          break;

        case ST_EXIT2_DR:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_UPDATE_DR;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_SHIFT_DR;
            record[i].future_state = jtag_state;
          }
          break;

        case ST_UPDATE_DR:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_SELECT_DR_SCAN;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_RUN_TEST_IDLE;
            record[i].future_state = jtag_state;
          }
          break;

        case ST_SELECT_IR_SCAN:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_TEST_LOGIC_RESET;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_CAPTURE_IR;
            record[i].future_state = jtag_state;
          }
          break;

        case ST_CAPTURE_IR:
          record[i].current_state = jtag_state;
          if (!record[i].tms){
            jtag_state = ST_SHIFT_IR;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_EXIT1_IR;
            record[i].future_state = jtag_state;
          }
          break;

        case ST_SHIFT_IR:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_EXIT1_IR;
            record[i].future_state = jtag_state;
          } else {
            record[i].future_state = jtag_state;
          }
          break;

        case ST_EXIT1_IR:
          record[i].current_state = jtag_state;
          if (!record[i].tms){
            jtag_state = ST_PAUSE_IR;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_UPDATE_IR;
            record[i].future_state = jtag_state;
          }
          break;

        case ST_PAUSE_IR:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_EXIT2_IR;
            record[i].future_state = jtag_state;
          } else {
            record[i].future_state = jtag_state;
          }
          break;

        case ST_EXIT2_IR:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_UPDATE_IR;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_SHIFT_IR;
            record[i].future_state = jtag_state;
          }
          break;

        case ST_UPDATE_IR:
          record[i].current_state = jtag_state;
          if (record[i].tms){
            jtag_state = ST_SELECT_IR_SCAN;
            record[i].future_state = jtag_state;
          } else {
            jtag_state = ST_RUN_TEST_IDLE;
            record[i].future_state = jtag_state;
          }
          break;

        default:
          fprintf(stderr, "Error Invalid State\n");
      }
//print to screen      
      printf("%d,%d,%d,%d,%s,%s\n",
      record[i].spl, record[i].tms, record[i].tdi, record[i].tdo, 
      state_name_arr[record[i].current_state], 
      state_name_arr[record[i].future_state]);
//print to file 'output_file' spl,tms,tdi,tdo,current state,future state
      fprintf(output_file, "%d,%d,%d,%d,%s,%s\n", 
      record[i].spl, record[i].tms, record[i].tdi, record[i].tdo, 
      state_name_arr[record[i].current_state], 
      state_name_arr[record[i].future_state]);
    } //end main for loop
    fclose(output_file); //close output_file, finished writing
  } //end if statement
  else
  {
    perror(filename); //throw error if it doesn't work
  }
  return 0;
} //end of main

