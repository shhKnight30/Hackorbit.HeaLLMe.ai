import mongoose from 'mongoose';

const chatSchema = new mongoose.Schema({
    SessionId: {
        type:mongoose.Schema.Types.ObjectId,
        ref: "Session",
        required: true,
        unique: true,
    },
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
