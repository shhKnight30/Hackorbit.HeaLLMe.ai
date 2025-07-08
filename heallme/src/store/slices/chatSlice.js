import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from 'axios'

const initialState = {
    chatMessage : null,
    response : null,
    loading : false,
    error : null
}

export const getChatResponse = createAsyncThunk(
    'chat/get-response',
    async (message, {rejectWithValue}) => {
        try {
            // change the url whatever it is
            const response = await axios.post('/api/v1/chat/get-response',{message})
            return response.data
        } catch (error) {
            
        }
    }
)

export const chatSlice = createSlice({
    name : 'chat',
    initialState : initialState,
    reducers : {},
    extraReducers : (builder) => {
        builder
        .addCase(getChatResponse.pending , (state) => {
            state.error = null
            state.loading = true
        })
        .addCase(getChatResponse.fulfilled,(state,action) => {
            state.error = null
            state.loading = false
            state.response = action.payload.data
        })
        .addCase(getChatResponse.rejected, (state,action) => {
            state.loading = false
            state.error = action.payload.data
        })
    }
})


export default chatSlice.reducer