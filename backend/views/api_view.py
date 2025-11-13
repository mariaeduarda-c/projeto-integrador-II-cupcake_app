from flask import jsonify

class APIView:
    @staticmethod
    def render_success(data=None, message="Sucesso", status_code=200):
        response = {'message': message}
        if data is not None:
            response['data'] = data
        return jsonify(response), status_code

    @staticmethod
    def render_error(message="Erro", status_code=400):
        return jsonify({'message': message}), status_code

    @staticmethod
    def render_item(item, message="Item encontrado", status_code=200):
        if item:
            return APIView.render_success(item.to_dict(), message, status_code)
        return APIView.render_error("Item não encontrado", 404)

    @staticmethod
    def render_items(items, message="Itens encontrados", status_code=200):
        items_list = [item.to_dict() for item in items]
        return APIView.render_success(items_list, message, status_code)