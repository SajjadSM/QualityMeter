from antlr4 import *
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from qualitymeter.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

java_dataTypes_list = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'String']


class realationListener(JavaParserLabeledListener):
    def __init__(self):
        self.__currentClass = "None"
        self.__currentMethod = "None"
        self.__everyObjectAndItsClass = {}
        self.VariableDeclarator=""
        self.__nodes = []
        self.__edges = {}

    def getNodes(self):
        return self.__nodes

    def getEdges(self):
        return self.__edges

    # To Get the nodes (better to say Methods)---------------------------------------------------------------
    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__currentClass = ctx.IDENTIFIER().getText()
        # print('entered class is:', self.__currentClass)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.__currentMethod = ctx.IDENTIFIER().getText()
        self.__nodes.append(ctx.IDENTIFIER().getText()+':'+self.__currentClass)
        # print(self.__currentMethod)

    # To Get the edges (better to say relation between Methods)----------------------------------------------
    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        objectAddress = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().getText()
        objectClassAdress = ctx.typeType().getText()
        if objectClassAdress not in java_dataTypes_list:
            self.__everyObjectAndItsClass[objectAddress] = objectClassAdress
            # print(self.__everyObjectAndItsClass)

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if ctx.qualifiedName().IDENTIFIER(0).getText() == 'java':
            i = len(ctx.qualifiedName().IDENTIFIER())
            java_dataTypes_list.append(ctx.qualifiedName().IDENTIFIER(i - 1).getText())
            # print(ctx.qualifiedName().IDENTIFIER(i-1).getText())

    # def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
    #     self.VariableDeclarator = ctx.variableDeclaratorId().getText()
    #
    # def exitVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
    #     self.VariableDeclarator = 'none'

    def enterExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        className = self.__currentClass
        if '.' in ctx.expression().getText():
            return
        if ctx.expression().primary().getText() == 'this':
            if isinstance(ctx.methodCall(), type(None)):
                return
            else:
                className = self.__currentClass
        elif ctx.expression().primary().getText() not in self.__everyObjectAndItsClass.keys():
            return
        else:
            className = self.__everyObjectAndItsClass[ctx.expression().primary().getText()]

        if isinstance(ctx.methodCall(), type(None)):
            return
        else:
            methodName = ctx.methodCall().IDENTIFIER().getText()

        if self.__currentMethod+":"+self.__currentClass in self.__edges.keys():
            self.__edges[self.__currentMethod + ":" + self.__currentClass][1] += 1
        else:
            self.__edges[self.__currentMethod+":"+self.__currentClass] = [methodName+":"+className, 1]
        # print(self.__edges)

    def exitExpression3(self, ctx: JavaParserLabeled.Expression3Context):
        if 'super' in ctx.methodCall().getText():
            return

        if isinstance(ctx.methodCall(), type(None)):
            return
        else:
            methodName = ctx.methodCall().IDENTIFIER().getText()

        if self.__currentMethod + ":" + self.__currentClass in self.__edges.keys():
            self.__edges[self.__currentMethod + ":" + self.__currentClass][1] += 1
        else:
            self.__edges[self.__currentMethod + ":" + self.__currentClass] = [methodName + ":" + self.__currentClass, 1]
        # print(self.__edges)
