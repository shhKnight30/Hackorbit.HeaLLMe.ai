import React, { useState, useRef } from 'react';
import { Paperclip, X } from 'lucide-react';

const UploadSection = ({ onFileSelect }) => {
  const [showOptions, setShowOptions] = useState(false);
  const [preview, setPreview] = useState(null);
  const imageRef = useRef();
  const docRef = useRef();

  const handleFileChange = (e, type) => {
    const file = e.target.files[0];
    if (!file) return;

    setShowOptions(false);
    setPreview({
      type,
      file,
      previewUrl: type === 'image' ? URL.createObjectURL(file) : null,
    });

    if (onFileSelect) onFileSelect(file);
  };

  const clearPreview = () => {
    setPreview(null);
    imageRef.current.value = '';
    docRef.current.value = '';
  };

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setShowOptions(!showOptions)}
        className="text-gray-500 hover:text-blue-600 p-2"
      >
        <Paperclip size={22} />
      </button>


      {showOptions && (
        <div className="absolute bottom-10 left-0 bg-white shadow-md rounded-md p-2 z-10 space-y-2 w-40">
          <button
            className="text-sm w-full text-left hover:bg-gray-100 px-2 py-1 rounded"
            onClick={() => imageRef.current.click()}
          >
            📷 Upload Image
          </button>
          <button
            className="text-sm w-full text-left hover:bg-gray-100 px-2 py-1 rounded"
            onClick={() => docRef.current.click()}
          >
            📄 Upload Document
          </button>
        </div>
      )}
      <input
        type="file"
        ref={imageRef}
        accept="image/*"
        className="hidden"
        onChange={(e) => handleFileChange(e, 'image')}
      />
      <input
        type="file"
        ref={docRef}
        accept=".pdf,.doc,.docx"
        className="hidden"
        onChange={(e) => handleFileChange(e, 'document')}
      />

      {preview && (
        <div className="absolute bottom-16 left-0 bg-gray-100 border rounded-md p-2 shadow w-60 flex items-center justify-between">
          {preview.type === 'image' ? (
            <img src={preview.previewUrl} alt="preview" className="w-12 h-12 object-cover rounded" />
          ) : (
            <div className="text-sm font-medium truncate w-44">{preview.file.name}</div>
          )}
          <button onClick={clearPreview} className="text-gray-500 hover:text-red-500">
            <X size={18} />
          </button>
        </div>
      )}
    </div>
  );
};

export default UploadSection;
