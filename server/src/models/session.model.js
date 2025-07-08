
import mongoose from "mongoose";

const sessionSchema = new mongoose.Schema({
  SessionId: {
    type: String,
    required: true,
    unique: true
  },
},{
    timestamps: {
         type: Date, default: Date.now 
    }
});

export default mongoose.model("Session", sessionSchema);
