import Combine
import Foundation
import SwiftUI
import UIKit

// Models
struct User: Codable {
    let id: String
    let email: String
    let token: String
}

struct AuthResponse: Codable {
    let access_token: String
}

struct ApiError: Codable {
    let message: String
}

// ViewModels
class AuthViewModel: ObservableObject {
    @Published var username = ""
    @Published var email = ""
    @Published var password = ""
    @Published var errorMessage = ""
    @Published var isAuthenticated = false
    @Published var isLoading = false

    func login() async {
        isLoading = true
        do {
            let url = URL(string: "http://0.0.0.0:8000/login/")!
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue(
                "application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")

            // Create form data (FastAPI's OAuth2PasswordRequestForm expects 'username' and 'password')
            let formData = "username=\(email)&password=\(password)"
                .addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)!
            request.httpBody = formData.data(using: .utf8)

            let (data, response) = try await URLSession.shared.data(for: request)

            // Print response for debugging
            if let responseString = String(data: data, encoding: .utf8) {
                print("Response: \(responseString)")
            }

            guard let httpResponse = response as? HTTPURLResponse else {
                throw URLError(.badServerResponse)
            }

            if httpResponse.statusCode == 200 {
                let response = try JSONDecoder().decode(AuthResponse.self, from: data)
                await MainActor.run {
                    UserDefaults.standard.set(response.access_token, forKey: "authToken")
                    self.isAuthenticated = true
                    self.isLoading = false
                }
            } else {
                // Try to decode error message
                let errorResponse = try? JSONDecoder().decode(ApiError.self, from: data)
                await MainActor.run {
                    self.errorMessage =
                        errorResponse?.message ?? "Login failed: \(httpResponse.statusCode)"
                    self.isLoading = false
                }
            }
        } catch {
            await MainActor.run {
                self.errorMessage = "Login error: \(error.localizedDescription)"
                self.isLoading = false
            }
        }
    }

    func register() async {
        isLoading = true
        do {
            let url = URL(string: "http://0.0.0.0:8000/register/")!
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue(
                "application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")

            // Create form data
            let formData = "username=\(username)&email=\(email)&password=\(password)"
                .addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)!
            request.httpBody = formData.data(using: .utf8)

            let (data, response) = try await URLSession.shared.data(for: request)

            // Print response for debugging
            if let responseString = String(data: data, encoding: .utf8) {
                print("Response: \(responseString)")
            }

            guard let httpResponse = response as? HTTPURLResponse else {
                throw URLError(.badServerResponse)
            }

            if httpResponse.statusCode == 200 {
                let response = try JSONDecoder().decode(AuthResponse.self, from: data)
                await MainActor.run {
                    UserDefaults.standard.set(response.access_token, forKey: "authToken")
                    self.isAuthenticated = true
                    self.isLoading = false
                }
            } else {
                // Try to decode error message
                let errorResponse = try? JSONDecoder().decode(ApiError.self, from: data)
                await MainActor.run {
                    self.errorMessage =
                        errorResponse?.message ?? "Registration failed: \(httpResponse.statusCode)"
                    self.isLoading = false
                }
            }
        } catch {
            await MainActor.run {
                self.errorMessage = "Registration error: \(error.localizedDescription)"
                self.isLoading = false
            }
        }
    }
}

class ImageUploadViewModel: ObservableObject {
    @Published var selectedImage: UIImage?
    @Published var analysisResult: String?
    @Published var isLoading = false
    @Published var errorMessage: String?

    func uploadImage() async {
        guard let image = selectedImage else { return }

        await MainActor.run {
            self.isLoading = true
        }

        do {
            let imageData = image.jpegData(compressionQuality: 0.8)!

            var request = URLRequest(url: URL(string: "http://0.0.0.0:8000/analyze-emotion/")!)
            request.httpMethod = "POST"

            let boundary = "Boundary-\(UUID().uuidString)"
            request.setValue(
                "multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

            var body = Data()

            // Add the file data
            body.append("\r\n--\(boundary)\r\n".data(using: .utf8)!)
            body.append(
                "Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n".data(
                    using: .utf8)!)
            body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
            body.append(imageData)
            body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

            request.httpBody = body

            let (data, _) = try await URLSession.shared.data(for: request)
            let result = try JSONDecoder().decode([String: String].self, from: data)

            await MainActor.run {
                self.analysisResult = result["emotion"]  // Changed from "analysis" to "emotion" to match API response
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
}

// Views
struct LoginView: View {
    @StateObject private var viewModel = AuthViewModel()

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    Text("Welcome")
                        .font(.largeTitle)
                        .padding()

                    TextField("Email", text: $viewModel.email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .autocapitalization(.none)

                    SecureField("Password", text: $viewModel.password)
                        .textFieldStyle(RoundedBorderTextFieldStyle())

                    if !viewModel.errorMessage.isEmpty {
                        Text(viewModel.errorMessage)
                            .foregroundColor(.red)
                            .padding()
                    }

                    Button(action: {
                        Task {
                            await viewModel.login()
                        }
                    }) {
                        if viewModel.isLoading {
                            ProgressView()
                        } else {
                            Text("Login")
                                .frame(maxWidth: .infinity)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(viewModel.isLoading)

                    NavigationLink("Create Account", destination: RegistrationView())
                        .padding()
                }
                .padding()
                .navigationBarHidden(true)
            }
            .ignoresSafeArea(.keyboard)
        }
        .fullScreenCover(isPresented: $viewModel.isAuthenticated) {
            ImageUploadView()
        }
    }
}

struct RegistrationView: View {
    @StateObject private var viewModel = AuthViewModel()
    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                Text("Create Account")
                    .font(.largeTitle)
                    .padding()

                TextField("Username", text: $viewModel.username)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .autocapitalization(.none)

                TextField("Email", text: $viewModel.email)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .autocapitalization(.none)

                SecureField("Password", text: $viewModel.password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())

                if !viewModel.errorMessage.isEmpty {
                    Text(viewModel.errorMessage)
                        .foregroundColor(.red)
                        .padding()
                }

                Button(action: {
                    Task {
                        await viewModel.register()
                    }
                }) {
                    if viewModel.isLoading {
                        ProgressView()
                    } else {
                        Text("Register")
                            .frame(maxWidth: .infinity)
                    }
                }
                .buttonStyle(.borderedProminent)
                .disabled(viewModel.isLoading)
            }
            .padding()
        }
        .ignoresSafeArea(.keyboard)
    }
}

struct ImageUploadView: View {
    @StateObject private var viewModel = ImageUploadViewModel()
    @State private var isImagePickerPresented = false
    @State private var sourceType: UIImagePickerController.SourceType = .photoLibrary

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                if let image = viewModel.selectedImage {
                    Image(uiImage: image)
                        .resizable()
                        .scaledToFit()
                        .frame(height: 300)

                    if viewModel.isLoading {
                        ProgressView()
                    }

                    if !viewModel.isLoading && viewModel.analysisResult == nil {
                        Button("Analyze Image") {
                            Task {
                                await viewModel.uploadImage()
                            }
                        }
                        .buttonStyle(.borderedProminent)
                    }

                    if let result = viewModel.analysisResult {
                        Text("Recognized emotion: \(result)")
                            .padding()
                    }

                    Button("Reset") {
                        viewModel.selectedImage = nil
                        viewModel.analysisResult = nil
                    }
                    .buttonStyle(.bordered)
                    .padding()

                    if let error = viewModel.errorMessage {
                        Text(error)
                            .foregroundColor(.red)
                            .padding()
                    }
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
            .navigationTitle("Know Your Mood")
            .sheet(isPresented: $isImagePickerPresented) {
                ImagePicker(selectedImage: $viewModel.selectedImage, sourceType: sourceType)
            }
        }
    }
}

// Helper Views
struct ImagePicker: UIViewControllerRepresentable {
    @Binding var selectedImage: UIImage?
    let sourceType: UIImagePickerController.SourceType
    @Environment(\.presentationMode) var presentationMode

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.delegate = context.coordinator
        picker.sourceType = sourceType
        return picker
    }

    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: ImagePicker

        init(_ parent: ImagePicker) {
            self.parent = parent
        }

        func imagePickerController(
            _ picker: UIImagePickerController,
            didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey: Any]
        ) {
            if let image = info[.originalImage] as? UIImage {
                parent.selectedImage = image
            }
            parent.presentationMode.wrappedValue.dismiss()
        }

        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.presentationMode.wrappedValue.dismiss()
        }
    }
}
