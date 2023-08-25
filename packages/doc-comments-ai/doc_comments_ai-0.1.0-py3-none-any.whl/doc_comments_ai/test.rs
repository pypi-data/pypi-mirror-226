/// Returns the programming language associated with the given file extension.
///
/// # Arguments
///
/// * `file_extension` - A string representing the file extension.
///
/// # Returns
///
/// The programming language associated with the file extension. If no mapping exists, `Language::UNKNOWN` is returned.
fn get_programming_language(file_extension: &str) -> Language {
    // Create a hash map to map file extensions to programming languages
    let language_mapping: std::collections::HashMap<&str, Language> = [
        (".py", Language::PYTHON),     // Python
        (".js", Language::JAVASCRIPT), // JavaScript
        (".ts", Language::TYPESCRIPT), // TypeScript
        (".java", Language::JAVA),     // Java
        (".kt", Language::KOTLIN),     // Kotlin
        (".lua", Language::LUA),       // Lua
    ]
    .iter()
    .cloned()
    .collect();

    // Return the programming language associated with the file extension,
    // or `Language::UNKNOWN` if no mapping exists
    *language_mapping
        .get(file_extension)
        .unwrap_or(&Language::UNKNOWN)
}

/// Extracts the file extension from a given file name.
///
/// # Arguments
///
/// * `file_name` - The name of the file.
///
/// # Returns
///
/// * The file extension if it exists, otherwise an empty string.
fn get_file_extension(file_name: &str) -> &str {
    // Check if the last dot exists in the file name
    if let Some(last_dot_index) = file_name.rfind('.') {
        // Return a string slice from the index of the last dot till the end
        &file_name[last_dot_index..]
    } else {
        // If no dot is found, return an empty string
        ""
    }
}
