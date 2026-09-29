import {createSlice} from "@reduxjs/toolkit";
const slice=createSlice({name:"booking",initialState:{current:null,selectedSeats:[]},reducers:{
 setCurrent:(s,a)=>{s.current=a.payload},setSeats:(s,a)=>{s.selectedSeats=a.payload},clear:(s)=>{s.current=null;s.selectedSeats=[]}
}});
export const {setCurrent,setSeats,clear}=slice.actions; export default slice.reducer;
