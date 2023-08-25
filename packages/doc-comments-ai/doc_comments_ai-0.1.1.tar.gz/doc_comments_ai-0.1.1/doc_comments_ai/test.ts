import * as fs from 'fs';
import * as path from 'path';

enum Language {
  PYTHON,
  JAVASCRIPT,
  TYPESCRIPT,
  JAVA,
  KOTLIN,
  LUA,
  RUST,
  GO,
  UNKNOWN
}

function getProgrammingLanguage(fileExtension: string): Language {
  const languageMapping: Record<string, Language> = {
    '.py': Language.PYTHON,
    '.js': Language.JAVASCRIPT,
    '.ts': Language.TYPESCRIPT,
    '.java': Language.JAVA,
    '.kt': Language.KOTLIN,
    '.lua': Language.LUA,
    '.rs': Language.RUST,
    '.go': Language.GO
  };

  return languageMapping[fileExtension] || Language.UNKNOWN;
}

function getFileExtension(fileName: string): string {
  return path.extname(fileName);
}

function writeCodeSnippetToFile(filePath: string, originalCode: string, modifiedCode: string): void {
  const fileContent: string = fs.readFileSync(filePath, 'utf-8');
  const startPos: number = fileContent.indexOf(originalCode);

  if (startPos !== -1) {
    const endPos: number = startPos + originalCode.length;
    const modifiedContent: string = fileContent.slice(0, startPos) + modifiedCode + fileContent.slice(endPos);

    fs.writeFileSync(filePath, modifiedContent, 'utf-8');
  }
}


function getBoldText(text: string): string {
  return `\u001b[01m${text}\u001b[0m`;
}
