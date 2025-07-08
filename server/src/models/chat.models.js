import mongoose from 'mongoose';

const chatSchema = new mongoose.Schema({
  refreshToken : { type: String, required: true }, 
  messages: [
    {
      role: {
        type:String,
        enum:["user","assistent"]
    }
    ,

        content: {
            type:String
            },
      timestamp: { type: Date, default: Date.now }
    }
  ]
}, { timestamps: true });

export default mongoose.model("Chat", chatSchema);
