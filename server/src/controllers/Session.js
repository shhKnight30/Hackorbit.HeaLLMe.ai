import asynchandler from "../utils/asynchandler.js";
import ApiError from "../utils/ApiError.js";
import ApiResponse from "../utils/apiresponse.js"; 
import sessionModels from "../models/session.models.js";
import { v4 as uuidv4 } from "uuid";

const createSession = asynchandler(async (req, res) => {
  const sessionId = uuidv4();
  const newsession= new sessionModels({sessionId})
  await newsession.save();

    res.status(201).json(new ApiResponse(200, "Session created successfully", { sessionId }));
})

const getSessionById = asynchandler(async (req, res) => {
    const { sessionId } = req.params;
    const session = await sessionModels.findOne({ sessionId });
    if (!session) {
        throw new ApiError(404, "Session not found");
    }

    res.status(200).json(new ApiResponse(200, "Session retrieved successfully", session));
})

const deleteSession= asynchandler(async (req, res) => {
    const { sessionId } = req.params;

    const session = await sessionModels.findOneAndDelete({ sessionId });
    if (!session) {
        throw new ApiError(404, "Session not found");
    }

    res.status(200).json(new ApiResponse(200, "Session deleted successfully", null));
})

export {
    createSession,
    getSessionById,
    deleteSession
}