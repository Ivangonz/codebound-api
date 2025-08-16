class MeController < ApplicationController
  include Authentication
  before_action :authenticate_user_with_jwt!

  def show
    render json: {
      user: {
        sub: @current_user_claims["sub"],
        email: @current_user_claims["email"]
      }
    }
  end
end
