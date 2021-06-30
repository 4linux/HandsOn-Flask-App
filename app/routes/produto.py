from bson.objectid import ObjectId
from flask import Blueprint, render_template, request, session
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from ..extentions.database import mongo

produto = Blueprint("produto", __name__, url_prefix="/produtos")


@produto.route("/list")
def listProdutos():
    if "username" in session:
        produtos = mongo.db.produtos.find()
        return render_template("produtos/list.html", produtos=produtos)
    else:
        return redirect(url_for("usuario.index"))


@produto.route("/insert", methods=["GET", "POST"])
def inserirProduto():
    if request.method == "GET":
        return render_template("produtos/insert.html")
    else:
        nome = request.form.get("nome")
        quantidade = request.form.get("quantidade")
        preco = request.form.get("preco")
        categoria = request.form.get("categoria")
        estoque = request.form.get("estoque")

        if not nome or len(nome) > 50:
            flash("Campo 'nome' é obrigatório")
        elif not quantidade or not quantidade.isdigit() or int(quantidade) < 0:
            flash("Campo 'quantidade' é obrigatorio.")
        elif not categoria:
            flash("Campo 'categoria' é obrigatório.")
        elif not estoque:
            flash("Campo 'estoque' é obrigatório.")
        elif not preco:
            flash("Campo 'preco' é obrigatorio ")
        else:
            mongo.db.produtos.insert_one(
                {
                    "produto": nome,
                    "estoque": estoque,
                    "categoria": categoria,
                    "quantidade": quantidade,
                    "preco": preco,
                    "valor_total": (float(quantidade) * float(preco))     
                }
            )
            flash('Produto criado com sucesso')
        return redirect(url_for("produto.listProdutos"))


@produto.route("/edit", methods=["GET", "POST"])
def editarProduto():
    if request.method == "GET":
        idproduto = request.values.get("idproduto")

        if not idproduto:
            flash("Campo 'idproduto' é obrigatório.")
            return redirect(url_for("produto.listProdutos"))
        else:
            idp = mongo.db.produtos.find({"_id": ObjectId(idproduto)})
            produto = [i for i in idp]
            estoques = set()
            produtos = mongo.db.produtos.find()
            for pr in produtos:
                estoques.add(pr["estoque"])
            return render_template(
                "produtos/edit.html", produto=produto, estoques=estoques
            )
    else:
        idproduto = request.form.get("idproduto")
        nome = request.form.get("nome", "")
        categoria = request.form.get("categoria", "")
        estoque = request.form.get("estoque", "")
        preco = request.form.get("preco", "")
        quantidade = request.form.get("quantidade", "")

        categorias = ["Informática", "Papelaria"]

        if not idproduto:
            flash("Campo 'idproduto' é obrigatório e deve ser numérico.")

        elif not nome or len(nome) > 40:
            flash("Campo 'nome' é obrigatório e deve ter no máximo 40 caracteres.")

        elif not quantidade or not quantidade.isdigit() or int(quantidade) < 0:
            flash("Campo 'quantidade' é obrigatório e deve ser numérico.")

        elif not categoria or categoria not in categorias:
            flash("Campo 'categoria' é obrigatório ou é inválido.")
        elif not preco:
            flash("Campo 'preco' é obrigatorio ")
        else:
            total = float(preco) * float(quantidade)
            update = mongo.db.produtos.update(
                {"_id": ObjectId(idproduto)},
                {
                    "$set": {
                        "produto": nome,
                        "categoria": categoria,
                        "estoque": estoque,
                        "quantidade": quantidade,
                        "preco": preco,
                        "valor_total": total,
                    }
                },
            )
            flash("Produto alterado com sucesso!")
        return redirect(url_for("produto.listProdutos"))


@produto.route("/delete")
def deletarProduto():
    idproduto = request.values.get("idproduto", "")
    if not idproduto:
        flash("Campo 'idproduto' é obrigatório.")
    else:
        delete = mongo.db.produtos.delete_one({"_id": ObjectId(idproduto)})
    return redirect(url_for("produto.listProdutos"))
