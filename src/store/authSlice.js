import {createSlice} from "@reduxjs/toolkit";
const slice=createSlice({name:"auth",initialState:{user:null,token:localStorage.getItem("token")},reducers:{
  setAuth:(s,a)=>{s.user=a.payload.user;s.token=a.payload.token},
  logout:(s)=>{s.user=null;s.token=null;localStorage.removeItem("token")}
}});
export const {setAuth,logout}=slice.actions; export default slice.reducer;
