//
//  ContentView.swift
//  knowyourmood
//
//  Created by Arkadiusz Juszczyk on 09/11/2024.
//

import SwiftUI
import UIKit

struct ContentView: View {
    @State private var selectedImage: UIImage?
    @State private var isImagePickerPresented = false
    @State private var sourceType: UIImagePickerController.SourceType = .photoLibrary

    var body: some View {
        VStack(spacing: 20) {
            Text("Welcome to Know Your Mood!")
                .font(.title)
                .multilineTextAlignment(.center)

            if let image = selectedImage {
                Image(uiImage: image)
                    .resizable()
                    .scaledToFit()
                    .frame(height: 300)

                Button("Upload") {
                    // Add upload logic here
                }
                .buttonStyle(.borderedProminent)
            } else {
                VStack(spacing: 16) {
                    Button("Choose from Gallery") {
                        sourceType = .photoLibrary
                        isImagePickerPresented = true
                    }
                    .buttonStyle(.bordered)

                    Button("Take a Photo") {
                        sourceType = .camera
                        isImagePickerPresented = true
                    }
                    .buttonStyle(.bordered)
                }
            }
        }
        .padding()
        .sheet(isPresented: $isImagePickerPresented) {
            ImagePicker(selectedImage: $selectedImage, sourceType: sourceType)
        }
    }
}

#Preview {
    ContentView()
}
