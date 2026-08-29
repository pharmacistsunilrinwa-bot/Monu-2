import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';

class AttachmentService {
  final ImagePicker _picker = ImagePicker();

  Future<XFile?> pickFile(ImageSource source, bool isVideo) async {
    try {
      if (isVideo) {
        return await _picker.pickVideo(source: source);
      } else {
        return await _picker.pickImage(source: source);
      }
    } catch (e) {
      debugPrint("Error picking file: $e");
      return null;
    }
  }

  String getMimeType(XFile file, bool isVideo) {
    final extension = file.path.split('.').last.toLowerCase();
    String mimeType = isVideo ? "video/mp4" : "image/jpeg";
    if (extension == "png") mimeType = "image/png";
    else if (extension == "gif") mimeType = "image/gif";
    else if (extension == "webp") mimeType = "image/webp";
    else if (extension == "mov") mimeType = "video/quicktime";
    else if (extension == "avi") mimeType = "video/x-msvideo";
    return mimeType;
  }
}
