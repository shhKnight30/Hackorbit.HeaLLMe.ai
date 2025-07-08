import mongoose from "mongoose";

const SymptomsSchema = new mongoose.Schema({
    SessionId: {
            type:mongoose.Schema.Types.ObjectId,
            ref: "Session",
            required: true,
            unique: true,
        },
    symptom: {
        type: String,
        required: true
    },
    severity: {
        type: String,
        enum: ["mild", "moderate", "severe"],
        required: true
    },
    duration: {
        type: String,
        required: true
    },
},{
    timestamps: true
})

export default mongoose.model("Symptoms", SymptomsSchema);