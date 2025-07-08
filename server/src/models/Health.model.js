import mongoose from "mongoose";

const healthSchema = new mongoose.Schema({
    SessionId: {
        type:mongoose.Schema.Types.ObjectId,
        ref: "Session",
        required: true,
        unique: true,
    },
    reports:{
        type: String,
        required: true
    },
    symptoms: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: "Symptoms",
        required: true
    }],
    medications:[
        {
            name: {
                type: String,
                required: true
            },
            dosage: {
                type: String,
                required: true
            },
            frequency: {
                type: String,
                required: true
            }
        }
    ]
},{
    timestamps: true
})

export default mongoose.model("Health", healthSchema);