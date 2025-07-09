import asynchandler from "../utils/asynchandler.js";
import ApiError from "../utils/ApiError.js";
import ApiResponse from "../utils/apiresponse.js"; 
import chatModels from "../models/chat.models.js";

const createMessage = asynchandler(async (req, res) => {
    const {sessionId, role, content} = req.body;
    if (!sessionId || !role || !content) {
        throw new ApiError(400, "All fields are required");
    }
    const newMessage = await chatModels.create({
        sessionId,
        messages: [{
            role,
            content,
            timestamp: new Date()
        }]
    });
    messages = newMessage.messages;
    res.status(201).json(new ApiResponse(200, "Message created successfully", messages));
})

const getMessagesBySessionId = asynchandler(async (req, res) => {
    const {sessionId} = req.params;
    const chat = await chatModels.findOne({sessionId}).populate('messages');
    if (!chat) {
        throw new ApiError(404, "Chat not found");
    }
    res.status(200).json(new ApiResponse(200, "Messages retrieved successfully", chat.messages));
})

const updateMessage = asynchandler(async (req, res) => {
    const {sessionId, messageId} = req.params;
    const {role, content} = req.body;

    if (!role || !content) {
        throw new ApiError(400, "All fields are required");
    }

    const chat = await chatModels.findOneAndUpdate(
        {sessionId, "messages._id": messageId},
        {$set: {"messages.$.role": role, "messages.$.content": content}},
        {new: true}
    );

    if (!chat) {
        throw new ApiError(404, "Message not found");
    }

    res.status(200).json(new ApiResponse(200, "Message updated successfully", chat.messages));
})

const deleteMessage = asynchandler(async (req, res) => {
    const {sessionId, messageId} = req.params;

    const chat = await chatModels.findOneAndUpdate(
        {sessionId},
        {$pull: {messages: {_id: messageId}}},
        {new: true}
    );

    if (!chat) {
        throw new ApiError(404, "Message not found");
    }

    res.status(200).json(new ApiResponse(200, "Message deleted successfully", []));
})

export {
    createMessage,
    getMessagesBySessionId,
    updateMessage,
    deleteMessage
};